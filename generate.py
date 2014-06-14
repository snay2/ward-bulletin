import argparse
from Cheetah.Template import Template
from bulletin import Bulletin

def get_template(template):
    f = open(template, 'r')
    t = f.read()
    f.close()
    return t

def render_template(template, input):
    template = get_template(template)
    return Template(template, searchList=[input]).__str__()

def write_to_file(filename, output):
    f = open(filename, 'w')
    f.write(output)
    f.close()

def generate(input_json, template_tex, output_tex):
    print 'Starting bulletin creation'
    print 'Loading JSON configuration %s' % input_json
    bulletin = Bulletin(input_json)
    print 'Writing output to %s' % output_tex
    write_to_file(output_tex, render_template(template_tex, bulletin.get_parameters()))
    print 'Done'

def main():
    parser = argparse.ArgumentParser(description='Generate a LaTeX ward bulletin from the given configs')
    parser.add_argument('--template', default='template.tex', help='LaTeX template file with Cheetah placeholders')
    parser.add_argument('--output', default='bulletin.tex', help='output file destination (default bulletin.tex)')
    parser.add_argument('input_file', help='JSON config file')
    args = vars(parser.parse_args())
    generate(args['input_file'], args['template'], args['output'])

if __name__=='__main__':
    main()

