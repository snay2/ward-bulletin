import sys
import os
import json
from datetime import datetime, timedelta
#import jinja2
from Cheetah.Template import Template

def get_template(template):
    # If I can figure out how to use Jinja2 again, here's the code:
    #jinja_env = jinja2.Environment(
    #        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    #return jinja_env.get_template(template)
    f = open(template, 'r')
    t = f.read()
    f.close()
    return t

def render_template(template, input):
    template = get_template(template)
    #return template.render(input)
    return Template(template, searchList=[input]).__str__()

def write_to_file(filename, output):
    f = open(filename, 'w')
    f.write(output)
    f.close()

def load_json(filename):
    f = open(filename, 'r')
    input = json.load(f)
    f.close()
    return input

def is_this_week(date_to_test, this_sunday):
    sunday_p = datetime.strptime(this_sunday, "%d %B %Y")
    next_sunday_p = sunday_p + timedelta(days=7)
    date_to_test_p = datetime.strptime(date_to_test, "%d %B %Y")
    return date_to_test_p >= sunday_p and date_to_test_p < next_sunday_p

def is_next_week(date_to_test, this_sunday):
    first_sunday = datetime.strptime(this_sunday, "%d %B %Y") + timedelta(days=7)
    second_sunday = first_sunday + timedelta(days=7)
    date_to_test_p = datetime.strptime(date_to_test, "%d %B %Y")
    return date_to_test_p >= first_sunday and date_to_test_p < second_sunday

def before_this_week(date_to_test, this_sunday):
    date_to_test_p = datetime.strptime(date_to_test, "%d %B %Y")
    this_sunday_p = datetime.strptime(this_sunday, "%d %B %Y")
    return date_to_test_p <= this_sunday_p

def filter_lessons(lessons, bulletin_date):
    sunday_school = {}
    for lesson in lessons['sunday_school']:
        if is_this_week(lesson['date'], bulletin_date):
            sunday_school['this_week'] = lesson['lesson']
        elif is_next_week(lesson['date'], bulletin_date):
            sunday_school['next_week'] = lesson['lesson']
            break

    priesthood_rs = {}
    for lesson in lessons['priesthood_rs']:
        if is_this_week(lesson['date'], bulletin_date):
            priesthood_rs['this_week'] = lesson['lesson']
        elif is_next_week(lesson['date'], bulletin_date):
            priesthood_rs['next_week'] = lesson['lesson']
            break

    return sunday_school, priesthood_rs

def pretty_date(orig_date):
    orig_date_p = datetime.strptime(orig_date, "%d %B %Y")
    return orig_date_p.strftime("%A %d %B")

def filter_calendar(events, bulletin_date):
    calendar = {'this_week': [], 'next_week': []}
    for event in events:
        if is_this_week(event['date'], bulletin_date):
            event['date'] = pretty_date(event['date'])
            calendar['this_week'].append(event)
        elif is_next_week(event['date'], bulletin_date):
            event['date'] = pretty_date(event['date'])
            calendar['next_week'].append(event)

    return calendar

def filter_primary(all_weeks, bulletin_date):
    primary = {}
    for week in all_weeks:
        if is_this_week(week['date'], bulletin_date):
            primary['this_week'] = week
        elif is_next_week(week['date'], bulletin_date):
            primary['next_week'] = week
            break

    return primary

def filter_orgs(all_orgs, bulletin_date):
    orgs = []
    #TODO Can I refactor this to use a filter?
    for org in all_orgs:
        if before_this_week(org['start_date'], bulletin_date):
            orgs.append(org)
    return orgs

def generate(input_json, template_tex, output_tex):
    print 'Starting bulletin creation'
    print 'Loading JSON configuration %s' % input_json
    input = load_json(input_json)
    calendar = load_json(input['calendar_json'])
    organizations = load_json(input['org_json'])
    lessons = load_json(input['lessons_json'])
    primary = load_json(input['primary_json'])

    input['sunday_school'], input['priesthood_rs'] = filter_lessons(lessons, input['bulletin_date'])
    input['calendar'] = filter_calendar(calendar['events'], input['bulletin_date'])
    input['primary'] = filter_primary(primary['weeks'], input['bulletin_date'])
    input['orgs'] = filter_orgs(organizations['orgs'], input['bulletin_date'])

    print 'Writing output to %s' % output_tex
    write_to_file(output_tex, render_template(template_tex, input))
    print 'Done'

def main(argv):
    if len(argv) < 2:
        print 'Usage: generate.py input_file'
        exit(1)
    input_json = argv[1]
    generate(input_json, 'template.cheetah.tex', 'bulletin.tex')

if __name__=='__main__':
    main(sys.argv)

