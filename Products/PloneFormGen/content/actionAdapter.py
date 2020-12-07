"""actionAdapter -- A base adapter for form actions"""

__author__  = 'Steve McMahon <steve@dcn.org>'
__docformat__ = 'plaintext'

from zope.interface import implements

from Products.PloneFormGen.config import *

from AccessControl import ClassSecurityInfo

from Products.Archetypes.public import *
from Products.Archetypes.utils import shasattr

from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATContentTypes.content.schemata import finalizeATCTSchema
from Products.ATContentTypes.content.base import registerATCT
from Products.CMFCore.permissions import View, ModifyPortalContent

from Products.TALESField import TALESString

from Products.PloneFormGen import HAS_PLONE30
from Products.PloneFormGen.interfaces import IPloneFormGenActionAdapter

FormAdapterSchema = ATContentTypeSchema.copy() + Schema((
    TALESString('execCondition',
        schemata='overrides',
        searchable=0,
        required=0,
        validators=('talesvalidator',),
        default='',
        write_permission=EDIT_TALES_PERMISSION,
        read_permission=ModifyPortalContent,
        isMetadata=True, # just to hide from base view
        widget=StringWidget(label="Execution Condition",
            description="""
                A TALES expression that will be evaluated to determine whether or not
                to execute this action.
                Leave empty if unneeded, and the ection will be executed. 
                Your expression should evaluate as a boolean; return True if you wish
                the action to execute.
                PLEASE NOTE: errors in the evaluation of this expression will cause
                an error on form display.
            """,
            size=70,
            i18n_domain = "ploneformgen",
            label_msgid = "label_execcondition_text",
            description_msgid = "help_execcondition_text",
        ),
    ),
    ))

if not HAS_PLONE30:
    FormAdapterSchema['description'].schemata = 'metadata'
finalizeATCTSchema(FormAdapterSchema, folderish=True, moveDiscussion=False)

if HAS_PLONE30:
    # avoid showing unnecessary schema tabs
    for afield in ('description',
                   'subject', 
                   'relatedItems', 
                   'location', 
                   'language', 
                   'effectiveDate', 
                   'expirationDate', 
                   'creation_date', 
                   'modification_date', 
                   'creators', 
                   'contributors', 
                   'rights', 
                   'allowDiscussion', 
                   'excludeFromNav', ):
        FormAdapterSchema[afield].widget.visible = {'view':'invisible','edit':'invisible'}
        FormAdapterSchema[afield].schemata = 'default'


class FormActionAdapter(ATCTContent):
    """A base action adapter"""

    implements(IPloneFormGenActionAdapter)

    schema         =  FormAdapterSchema

    content_icon   = 'FormAction.gif'
    meta_type      = 'FormActionAdapter'
    portal_type    = 'FormActionAdapter'
    archetype_name = 'Form Action Adapter'

    immediate_view = 'base_view'
    default_view   = 'base_view'
    suppl_views = ()

    typeDescription= 'An adapter that supplies a form action.'

    global_allow = 0    

    security       = ClassSecurityInfo()


    def onSuccess(self, fields, REQUEST=None):
        """ called by form to invoke custom success processing """
        
        # fields will be a sequence of objects with an IPloneFormGenField interface
        
        pass


    def at_post_create_script(self):
        """ activate action adapter in parent folder """
        
        # XXX TODO - change to use events when we give up on Plone 2.1.x
        
        ATCTContent.at_post_create_script(self)

        self.aq_parent.addActionAdapter(self.id)
        
