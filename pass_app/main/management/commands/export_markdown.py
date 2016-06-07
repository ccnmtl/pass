import os

from django.core.management.base import BaseCommand
from django.test.client import RequestFactory
from pagetree.models import Hierarchy
from pagetree.tests.factories import UserFactory


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('dest',  help='Destination directory')

        parser.add_argument(
            '--hierarchy', dest='hierarchy', default='all',
            help='A specific hierarchy to export')

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
            self.image_directory = '{}static/img/'.format(self.dest)
            self.create_directory(self.image_directory)
        return self.image_directory

    def hierarchies(self, hierarchy_name):
        qs = Hierarchy.objects.all()
        if hierarchy_name != 'all':
            qs = qs.filter(name=hierarchy_name)
        return qs

    def section_as_yaml(self, module, idx, section, f):
        f.write('---\n')
        f.write('title: "{}"\n'.format(section.label.encode('utf8')))
        f.write('module: "{}"\n'.format(module.label.encode('utf8')))
        f.write('type: "module_page"\n')
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
            # frontmatter
            self.section_as_yaml(module, idx, section, f)

            # export the pageblocks
            for pb in section.pageblock_set.all():
                f.write('<h3>{}</h3>'.format(pb.label.encode('utf-8')))
                f.write('<div class="pageblock {}">'.format(pb.css_extra))
                f.write(pb.render(**self.render_context).encode('utf-8'))
                f.write('</div>')

        # export the children
        for child in section.get_children():
            idx = idx + 1
            self.export_section(module, idx, module_directory, child)

    def handle(self, *args, **options):
        self.dest = self.get_destination_directory(options['dest'])

        request = RequestFactory()
        request.user = UserFactory()
        self.render_context = {'request': request}

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
