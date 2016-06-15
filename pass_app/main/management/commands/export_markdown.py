import os
from urlparse import urlparse

from django.core.management.base import BaseCommand
from django.test.client import RequestFactory
from pagetree.models import Hierarchy
from pagetree.tests.factories import UserFactory

from bs4 import BeautifulSoup
import requests


class Command(BaseCommand):

    SHORTCODES = {
        'SpecialNeedsCallBlock':
            '{{< highlight html >}}<b>Special Needs Q&A</b>{{< /highlight >}}',
        'SupportServiceBlock':
            '{{< highlight html >}}<b>Support Services</b>{{< /highlight >}}',
        'InfographicBlock':
            '{{< highlight html >}}<b>Infographic</b>{{< /highlight >}}',
    }

    EXPORTABLE_BLOCKS = [
        'HTMLBlock', 'HTMLBlockWYSIWYG', 'ImageBlock', 'ImagePullQuoteBlock',
        'PullQuoteBlock', 'Quiz', 'TextBlock'
    ]

    POSTPROCESS_BLOCKS = [
        'HTMLBlock', 'HTMLBlockWYSIWYG', 'ImageBlock', 'ImagePullQuoteBlock',
        'TextBlock'
    ]

    def add_arguments(self, parser):
        parser.add_argument('dest',  help='Destination directory')

        parser.add_argument(
            '--hierarchy', dest='hierarchy', default='all',
            help='A specific hierarchy to export')

        parser.add_argument(
            '--media-url', dest='media_url', default='uploads',
            help='url for fully qualified media location, i.e. S3 url')

    def create_directory(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def get_destination_directory(self, dest):
        if not dest[-1] == '/':
            dest += '/'
        print 'Exporting to {}'.format(dest)
        return dest

    def get_or_create_content_directory(self):
        if not hasattr(self, 'content_directory'):
            self.content_directory = '{}content/'.format(self.dest)
            self.create_directory(self.content_directory)
        return self.content_directory

    def get_or_create_image_directory(self):
        if not hasattr(self, 'image_directory'):
            self.image_directory = '{}static/img/assets/'.format(self.dest)
            self.create_directory(self.image_directory)
        return self.image_directory

    def hierarchies(self, hierarchy_name):
        qs = Hierarchy.objects.all()
        if hierarchy_name != 'all':
            qs = qs.filter(name=hierarchy_name)
        return qs

    def postprocess_image(self, img):
        src = img.attrs['src']
        alt = img.attrs['alt'] if 'alt' in img.attrs else ''
        imgclass = ' '.join(img.attrs['class'] if 'class' in img.attrs else '')
        basename = os.path.basename(urlparse(src).path)

        filename = self.get_or_create_image_directory() + basename
        if not os.path.exists(filename):
            with open(filename, 'wb') as imagef:
                r = requests.get(src)
                for chunk in r:
                    imagef.write(chunk)
                print("saved image {}".format(filename))

        shortcode = '{{{{< figure src="/img/assets/{}"' + \
            ' alt="{}" class="{}" >}}}}'
        img.parent.append(shortcode.format(basename, alt, imgclass))

        img.extract()

    def postprocess_video(self, iframe):
        shortcode = '{{< youtube id="NWNxuJ0MK3k" >}}'
        iframe.parent.append(shortcode)
        iframe.extract()

    def postprocess(self, rendered):
        soup = BeautifulSoup(rendered)
        for tag in soup.findAll(True):
            if tag.name == 'img':
                self.postprocess_image(tag)
            elif tag.name == 'iframe':
                self.postprocess_video(tag)

        body = soup.find('body')
        body.hidden = True  # don't export the body tag
        return body.encode(formatter=None) if body else ''

    def export_block(self, f, type_name, pb):
        if pb.label:
            f.write('<h3>{}</h3>'.format(pb.label.encode('utf-8')))
        f.write('<div class="pageblock')
        if pb.css_extra:
            f.write(' ')
            f.write(pb.css_extra)
        f.write('">')

        rendered = pb.render(**self.render_context).encode('utf-8')
        if (len(rendered.strip()) > 0 and
                type_name in self.POSTPROCESS_BLOCKS):
            rendered = self.postprocess(rendered)

        f.write(rendered)
        f.write('</div>')

    def frontmatter(self, module, idx, section, f):
        f.write('---\n')
        f.write('title: "{}"\n'.format(section.label.encode('utf8')))
        f.write('module: "{}"\n'.format(module.label.encode('utf8')))
        f.write('type: "module-page"\n')
        f.write('ordinal: {}\n'.format(idx))
        f.write('depth: {}\n'.format(section.depth))

        nxt = section.get_next()
        if nxt and not nxt.is_root():
            f.write('next: "../{}/"\n'.format(nxt.slug))

        prev = section.get_previous()
        if prev and prev != module:
            f.write('previous: "../{}/"\n'.format(prev.slug))

        f.write('---\n')

    def export_section(self, module, idx, module_directory, section):
        # create a file in the content directory
        filename = '{}{}.md'.format(module_directory, section.slug)
        print filename

        with open(filename, 'w') as f:
            self.frontmatter(module, idx, section, f)

            # export pageblocks
            for pb in section.pageblock_set.all():
                blk = pb.block()
                type_name = type(blk).__name__

                if type_name in self.SHORTCODES:
                    f.write(self.SHORTCODES[type_name])
                    continue
                elif type_name not in self.EXPORTABLE_BLOCKS:
                    continue
                else:
                    self.export_block(f, type_name, pb)

        # export the section children
        for child in section.get_children():
            idx = idx + 1
            self.export_section(module, idx, module_directory, child)

    def handle(self, *args, **options):
        self.dest = self.get_destination_directory(options['dest'])

        request = RequestFactory()
        request.user = UserFactory()
        self.render_context = {
            'request': request,
            'MEDIA_URL': options['media_url']
        }

        try:
            # hierarchies to export
            hierarchies = self.hierarchies(options['hierarchy'])

            for hierarchy in hierarchies:
                # Match/Pass have a root node, followed by a content node
                # This export pattern will not work for all our pagetree apps
                module = hierarchy.get_root().get_first_child()
                module_directory = '{}{}/'.format(
                    self.get_or_create_content_directory(), module.slug)
                self.create_directory(module_directory)
                self.export_section(module, 1, module_directory, module)
        finally:
            request.user.delete()
