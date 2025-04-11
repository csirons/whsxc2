from django import template
from django.template import Variable

register = template.Library()

def gender_name(value):
  return {
    'F': 'Girls',
    'M': 'Boys',
  }[value]
register.filter('gender_name', gender_name)

def less_than(value, num):
  if not value:
    return False
  return value < int(num)
register.filter('less_than', less_than)

def have_team_place(meets):
  for meet in meets:
    if meet.team_place_male or meet.team_place_female:
      return True
  return False
register.filter('have_team_place', have_team_place)

def have_top_finish(meets):
  for meet in meets:
    if meet.top_finish_male or meet.top_finish_female:
      return True
  return False
register.filter('have_top_finish', have_top_finish)

def have_pack_time(meets):
  for meet in meets:
    if meet.pack_time_male or meet.pack_time_female:
      return True
  return False
register.filter('have_pack_time', have_pack_time)

def time_tba(time):
  if time.hour == 0 and time.minute == 0:
    return 'TBA'
  else:
    hour = time.hour
    ampm = 'am'
    if hour > 12:
      hour = hour - 12
      ampm = 'pm'
    return str(hour) + ':' + time.strftime('%M') + ampm
register.filter('time_tba', time_tba)

def grade_name(value):
  return {
    '1': 'Senior',
    '2': 'Junior',
    '3': 'Sophomore',
    '4': 'Freshman',
  }[str(value)]
register.filter('grade_name', grade_name)

def grade_name_plural(value):
  return {
    '1': 'Seniors',
    '2': 'Juniors',
    '3': 'Sophomores',
    '4': 'Freshmen',
  }[str(value)]
register.filter('grade_name_plural', grade_name_plural)

def team_name(value):
  return {
    '1GV': 'Girls Varsity',
    '2BV': 'Boys Varsity',
    '3GJ': 'Girls JV',
    '4BJ': 'Boys JV',
    '5GF': 'Girls Frosh/Soph',
    '6BF': 'Boys Frosh/Soph',
  }[value]
register.filter('team_name', team_name)

def convert_seconds(value):
  if str(value.__class__) == "<type 'unicode'>":
    return value
  else:
    return "%d:%02d" % (value/60,value%60)
register.filter('convert_seconds',convert_seconds)

def ifnotnull(value):
  if value:
    return value
  else:
    return ""
register.filter('ifnotnull',ifnotnull)

def list_runs(females, males, hide_date=None):
  return { 'female_runs': females, 'male_runs': males, 'hide_date': hide_date }
register.inclusion_tag('runners/runs_list.html')(list_runs)

def runs_list(females, males, title):
  return { 'female_runs': females, 'male_runs': males, 'title': title }
register.inclusion_tag('runners/_runs_list.html')(runs_list)

def meets_list(meets, show_year=None):
  return { 'meets': meets, 'show_year': show_year }
register.inclusion_tag('meets/_meets_list.html')(meets_list)

def load_runs(parser,token):
   return LoadRunsNode()

class LoadRunsNode(template.Node):
  def render(self, context):
    context['runs'] = context['race'].run_set.order_by(context['sort_runs_by'])
    return ''
register.tag('load_runs',load_runs)

def sectionbyattribute(parser,token):
  try:
    tag_name, attribute, objects_list = token.split_contents()
  except ValueError:
    raise template.TemplateSyntaxError("%r tag requires two arguments" % token.contents[0])

  node_list = parser.parse(('endsectionbyattribute',))
  parser.delete_first_token()
  return SectionByAttribute(attribute, objects_list, node_list)

class SectionByAttribute(template.Node):
  def __init__(self, attribute, objects_list, node_list):
    if attribute[0] == attribute[-1] and attribute[0] in ('"', "'"):
      self.attribute_name = self.attribute = attribute[1:-1]
      self.attribute_variable = None
    else:
      self.attribute = None
      self.attribute_name = attribute
      self.attribute_variable = template.Variable(attribute)
    self.objects_list = Variable(objects_list)
    self.objects_list_name = objects_list.replace('.','_')
    self.node_list = node_list

  def render(self, context):
    sections = []
    current_section = 0
    
    if self.attribute_variable:
      self.attribute = self.attribute_variable.resolve(context)
    
    for object in self.objects_list.resolve(context):
      attr = getattr(object,self.attribute)
      
      if callable(attr):
        attr = attr()
      
      if attr != current_section:
        current_section = attr
        sections.append( { self.attribute: current_section, self.objects_list_name: [] } )
      sections[-1][self.objects_list_name].append(object)

    output = ""
    for section in sections:
      context[self.attribute_name] = section
      output += self.node_list.render(context)
      del context[self.attribute_name]

    return output
register.tag('sectionbyattribute',sectionbyattribute)

def sum(parser,token):
  try:
    tag_name, list, field_name = token.split_contents()
  except ValueError:
    raise template.TemplateSyntaxError("%r tag requires two arguments" % token.contents[0])

  return SumNode(list,field_name)

class SumNode(template.Node):
  def __init__(self, list, field_name):
    self.list = Variable(list)
    self.field_name = field_name

  def render(self, context):
    sum = 0
    for item in self.list.resolve(context):
      sum += getattr(item,self.field_name)
    return str(sum)
register.tag('sum',sum)

def get_dict_value(parser,token):
  try:
    tag_name, key, fromWord, dict, asWord, name = token.split_contents()
  except ValueError:
    raise template.TemplateSyntaxError("%r tag requires five arguments" % token.contents[0])
  return GetDictValue(key, dict, name)

class GetDictValue(template.Node):
  def __init__(self, key, dict, name):
    if key[0] == key[-1] and key[0] in ('"', "'"):
      self.key_str = self.key = key[1:-1]
      self.key_variable = False
    else:
      self.key_str = False
      self.key_variable = template.Variable(key)
    self.dict = Variable(dict)
    self.name = name

  def render(self, context):
    if self.key_str:
      context[self.name] = self.dict.resolve(context)[self.key_str]
    else:
      context[self.name] = self.dict.resolve(context)[self.key_variable.resolve(context)]

    return ''
register.tag('get_dict_value',get_dict_value)

