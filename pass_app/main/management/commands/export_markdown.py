import os
from urlparse import urlparse

from bs4 import BeautifulSoup
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.test.client import RequestFactory
from pagetree.models import Hierarchy
from pagetree.tests.factories import UserFactory
import requests


class Command(BaseCommand):

    SHORTCODES = {
        'specialneedscallblock':
            '{{< interactives url="specialneedsvisit" width="900px"' +
            ' height="800px" >}}',
        'supportserviceblock':
            '{{< interactives url="supportservices" width="900px"' +
            ' height="800px" >}}',
        'infographicblock':
            '{{{{< interactives url="{}" width="900px"' +
            ' height="800px" >}}}}',
        'careermap':
            '{{{{< interactives url="careerplan/?actorIdx={}" width="900px"' +
            ' height="800px">}}}}',
        'proxyblock':
            '{{{{< interactives url="careerplan/?actorIdx={}" width="900px"' +
            ' height="800px" >}}}}',
        'careerlocationstrategyblock':
            '{{< interactives url="ruralhealth" width="900px"' +
            ' height="800px" >}}',
        'careerlocationblock':
            '{{< interactives url="dentaloffice" width="900px"' +
            ' height="800px" >}}',
    }

    EXPORTABLE_BLOCKS = [
        'htmlblock', 'htmlblockwysiwyg', 'imageblock', 'imagepullquoteblock',
        'pullquoteblock', 'quiz', 'textblock'
    ]

    POSTPROCESS_BLOCKS = [
        'htmlblock', 'htmlblockwysiwyg', 'imageblock', 'imagepullquoteblock',
        'textblock', 'quiz'
    ]

    # These sections are now extraneous due to multi-page javascript
    # interactions being distilled into one page. This is a bit hacky and
    # closely tied to the PASS hierarchy, but creates the ability to
    # generate the export without a need for postprocessing.
    DEPRECATED_SECTIONS = [
        # module_one
        'Sam',
        'Sam\'s Summary',
        'Sally',
        'Sally\'s Summary',
        'Your Career',
        'Your Summary',

        # module_two
        'Select a Practice Location',
        'Board of Director\'s Meeting',
        'Practice Location Report',

        # module_three
        'Select Strategy',
        'Defend Strategy',
        'Pros & Cons',
        'Rethink Strategy Selection',

        # all modules
        'Feedback'
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

    def has_quizzes(self, section):
        return section.pageblock_set.filter(
            content_type=self.quiz_type).count() > 0

    def has_interactives(self, section):
        return section.pageblock_set.filter(
            content_type__model__in=self.SHORTCODES.keys()).count() > 0

    def open_form(self, f, section):
        needs_form = (not self.has_interactives(section) and
                      self.has_quizzes(section))
        if needs_form:
            f.write('<form method="post" action=".">')
        return needs_form

    def close_form(self, f, needs_form):
        if needs_form:
            f.write('<div class="submit-container">'
                    '<input class="btn btn-info btn-submit-section" '
                    'type="submit" value="Submit" /></div>')
            f.write('</form>')

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
            elif tag.name == 'script':
                tag.extract()

        body = soup.find('body')
        body.hidden = True  # don't export the body tag
        return body.encode(formatter=None) if body else ''

    def write_shortcode(self, f, section, type_name):
        code = self.SHORTCODES[type_name]
        if type_name == 'careermap' or type_name == 'proxyblock':
            if section.label == 'Advise Sam':
                code = code.format(0)
            elif section.label == 'Advise Sally':
                code = code.format(1)
            else:
                code = code.format(2)
        elif type_name == 'infographicblock':
            if section.label == 'Scenario 1':
                code = code.format('elderdresser')
            else:
                code = code.format('elderfridge')

        f.write(code)

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

    def frontmatter(self, module, idx, section, f, prev, nxt):
        f.write('---\n')
        f.write('title: "{}"\n'.format(section.label.encode('utf8')))
        f.write('module: "{}"\n'.format(module.label.encode('utf8')))
        f.write('type: "module-page"\n')
        f.write('menu:\n')
        f.write('  {}:\n'.format(module.slug.replace('-', '_')))
        f.write('    parent: "{}"\n'.format(module.slug.replace('-', '_')))
        f.write('    weight: {}\n'.format(idx))
        f.write('depth: {}\n'.format(section.depth))

        if nxt:
            f.write('next: "../{}/"\n'.format(nxt.slug))

        if prev:
            f.write('previous: "../{}/"\n'.format(prev.slug))

        f.write('---\n')

    def export_section(self, module, module_dir, idx, section, prev, nxt):
        # create a file in the content directory
        filename = '{}{}.md'.format(module_dir, section.slug)
        print filename

        with open(filename, 'w') as f:
            self.frontmatter(module, idx, section, f, prev, nxt)

            # export pageblocks
            needs_form = self.open_form(f, section)

            for pb in section.pageblock_set.all():
                blk = pb.block()
                type_name = type(blk).__name__.lower()

                if type_name in self.SHORTCODES:
                    self.write_shortcode(f, section, type_name)
                    break
                elif type_name not in self.EXPORTABLE_BLOCKS:
                    continue
                elif type_name == 'quiz':
                    blk.rhetorical = True
                    self.export_block(f, type_name, pb)
                else:
                    self.export_block(f, type_name, pb)

            self.close_form(f, needs_form)

    def exportable_sections(self, module):
        sections = []
        for section in module.get_descendants():
            if (not section.is_root() and
                section.pageblock_set.all().count() > 0 and
                    section.label not in self.DEPRECATED_SECTIONS):
                sections.append(section)
        return sections

    def handle(self, *args, **options):
        self.dest = self.get_destination_directory(options['dest'])
        self.quiz_type = ContentType.objects.filter(model='quiz')

        request = RequestFactory()
        request.user = UserFactory()
        self.render_context = {
            'request': request,
            'MEDIA_URL': options['media_url']
        }

        try:
            for hierarchy in self.hierarchies(options['hierarchy']):
                # Match/Pass have a root node, followed by a content node
                # This export pattern will not work for all our pagetree apps
                module = hierarchy.get_root().get_first_child()
                d = '{}{}/'.format(
                    self.get_or_create_content_directory(), module.slug)
                self.create_directory(d)

                # construct an array of exportable sections
                prev = None
                nxt = None
                sections = self.exportable_sections(module)
                count = len(sections)
                for idx, section in enumerate(sections):
                    nextIdx = idx + 1
                    nxt = sections[nextIdx] if nextIdx < count else None
                    self.export_section(module, d, idx, section, prev, nxt)
                    prev = section
        finally:
            request.user.delete()
