# coding=UTF-8
from __future__ import print_function
from __future__ import unicode_literals
import sys
from lxml import etree as ET

#  
#  name: check_value_exists
#  @param filepath      Path to the codelist wee want to check
#  @param xpathString   xpath to the element we want to check
#  @param value         The value we want to check the existence of
#  @return yes/no
# 
def check_value_exists (filepath, xpathString, value):
  
  for items in ET.parse(filepath).getroot().findall('codelist-items'):
    values = items.xpath(xpathString)
    #print (', '.join(values))
    if value in values:
      print ('pass')
    else:
      print ('fail')

#  
#  name: check_value_does_not_exists
#  @param filepath      Path to the codelist wee want to check
#  @param xpathString   xpath to the element we want to check
#  @param value         The value we want to check does not exists
#  @return yes/no
#  

def check_value_does_not_exist (filepath, xpathString, value):
  
  for items in ET.parse(filepath).getroot().findall('codelist-items'):
    values = items.xpath(xpathString)
    #print (', '.join(values))
    if value in values:
      print ('fail')
    else:
      print ('pass')





#Test Description Type codelist changes
filepath = "../xml/DescriptionType.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Other')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Autre') #Check for the translation value
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','4')
check_value_exists(filepath,'//codelist-items/codelist-item/description/text()','For miscellaneous use. A further classification or breakdown may be included in the narrative')

#Test Activity Status codelist changes
filepath = "../xml/ActivityStatus.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Suspended')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Suspendu') #Check for the translation value
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','6')

#Test Transaction Type codelist changes
filepath = "../xml/TransactionType.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/description/text()','Funds received (whether from an external source or through internal accounting) for specific use on this activity.')

check_value_does_not_exist(filepath,'//codelist-items/codelist-item/description/text()','Funds received from an external funding source (eg a donor).')

##Test Related Activity Type codelist changes
filepath = "../xml/RelatedActivityType.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Third Party') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','5')
check_value_exists(filepath,'//codelist-items/codelist-item/description/text()','A report by another organisation on the same activity (excluding activities reported as part of financial transactions - eg. provider-activity-id - or a co-funded activity using code = 4)')

#Rename Multifunded on Related Activity Type codelist
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Co-funded') 
check_value_does_not_exist(filepath,'//codelist-items/codelist-item/name/text()','Multifunded')

check_value_exists(filepath,'//codelist-items/codelist-item/description/text()','An activity that receives funding from more than one organisation')
check_value_does_not_exist(filepath,'//codelist-items/codelist-item/description/text()','A multifunded, or co-funded activity. The identifier should be globally unique and shared by all reporters of this activity.')


#Test DocumentCategory codelist changes
filepath = "../xml/DocumentCategory.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Sector strategy') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','B11')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Thematic strategy') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','B12')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Country-level Memorandum of Understanding') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','B13')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Evaluations policy') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','B14')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','General Terms and Conditions') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','B15')

#Test Policy Marker codelist changes
filepath = "../xml/PolicyMarker.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Reproductive, Maternal, Newborn and Child Health (RMNCH)') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','9')

#Test Vocabulary codelist changes
filepath = "../xml/Vocabulary.xml"
print (filepath)
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()','Reporting Organisation (2) - where reporting organisations have more than one vocabulary that they wish to reference') 
check_value_exists(filepath,'//codelist-items/codelist-item/code/text()','RO2')
check_value_exists(filepath,'//codelist-items/codelist-item/name/text()',"Organisation déclarante (2) - dans le cas où les organisations déclarantes ont plus d'un vocabulaire qu'ils souhaitent faire référence") #Check for the translation value