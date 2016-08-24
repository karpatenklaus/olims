"""The request for analysis by a client. It contains analysis instances.
"""
import datetime
from base_olims_model import BaseOLiMSModel
from fields.string_field import StringField
from fields.text_field import TextField
from fields.boolean_field import BooleanField
from fields.date_time_field import DateTimeField
from fields.fixed_point_field import FixedPointField
from fields.widget.widget import StringWidget, TextAreaWidget, \
                                BooleanWidget, DateTimeWidget, \
                                DecimalWidget, RichWidget
from openerp import fields, models, api
from openerp.tools.translate import _
AR_STATES = (
    ('sample_registered','Sample Registered'),
    ('not_requested','Not Requested'),
    ('to_be_sampled','To Be Sampled'),
    ('sampled','Sampled'),
    ('to_be_preserved','To Be Preserved'),
    ('sample_due','Sample Due'),
    ('sample_received','Received'),
    ('attachment_due','Attachment Outstanding'),
    ('to_be_verified','To be verified'),
    ('verified','Verified'),
    ('published','Published'),
    ('invalid','Invalid'),
    )

schema = (fields.Char(string='RequestID',
                      compute='compute_analysisRequestId',
        ),
    fields.Many2one(string='Client',
                    comodel_name='olims.client',
                    required=False,

    ),
    fields.Many2one(string='Contact',
                    comodel_name='olims.contact',
                    relation='ar_contact',
                    required=True
    ),
    fields.Many2one(string='CCContact',
                    comodel_name='olims.contact',
                    relation='ar__cc_contact',
                    required=False
    ),
    StringField(
        'CCEmails',
    ),

    fields.Char(string='Sample',
                        compute='Compute_AnalysisSample',

    ),
    fields.Many2one(string='Sample_id',
                        comodel_name='olims.sample',

    ),
    fields.Many2one(string='Batch',
                        comodel_name='olims.batch',

    ),
    fields.Many2one(string='SubGroup',
                        comodel_name='olims.subgroup',
                        relation='ar_subgroup'

    ),
    fields.Many2one(string='Template',
                        comodel_name='olims.ar_template',

    ),
    fields.Many2one(string='AnalysisProfile',
                        comodel_name='olims.analysis_profile',
                        relation='ar_to_analysisprofile'

    ),
    fields.One2many(string='Partition',
                     comodel_name='olims.ar_partition',
                    inverse_name='analysis_request_id',
    ),
    fields.One2many(string='Sample Partition',
                     comodel_name='olims.ar_sample_partition',
                    inverse_name='analysis_request_id',
    ),
    fields.One2many(string='Analyses',
                     comodel_name='olims.ar_analysis',
                    inverse_name='analysis_request_id',
    ),
    # Sample field
    DateTimeField('DateSampled',
    ),
    # Sample field
    fields.Many2one(string='Sampler',
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,18])]",
    ),
    DateTimeField(
        'SamplingDate',
        required=1,
    ),
    fields.Many2one(string='SampleType',
                        comodel_name='olims.sample_type',
                        required=True

    ),
    fields.Many2one(string='Specification',
                        comodel_name='olims.analysis_spec',
                        relation='ar_analysis_spec',
                        required=False,
    ),
    fields.Many2one(string='SamplePoint',
                        comodel_name='olims.sample_point',

    ),
    fields.Many2one(string='StorageLocation',
                        comodel_name='olims.storage_location',

    ),
    StringField(
        'ClientOrderNumber',
    ),
    # Sample field
    StringField(
        'ClientReference',
        searchable=True,
    ),
    # Sample field
    StringField(
        'ClientSampleID',
        searchable=True,
    ),

    fields.Many2one(string='SamplingDeviation',
                        comodel_name='olims.sampling_deviation',

    ),
#     # Sample field
    fields.Many2one(string='SampleCondition',
                        comodel_name='olims.sample_condition',

    ),
    fields.Many2one(string='DefaultContainerType',
                        comodel_name='olims.container_type',

    ),
    # Sample field
    BooleanField(
        'AdHoc',
        default=False,
    ),
    # Sample field
    BooleanField(
        'Composite',
        default=False,
    ),
    BooleanField(
        'ReportDryMatter',
        default=False,
    ),
    BooleanField(
        'InvoiceExclude',
        default=False,
    ),
    DateTimeField(
        'DateReceived',
    ),
    DateTimeField(
        'DatePublished',
    ),
    DateTimeField(
        'DateDue',
    ),
    TextField(
        string='Remarks',
        searchable=True,
    ),
    FixedPointField(
        'MemberDiscount',
    ),
    fields.Many2one(string='ChildAnalysisRequest',
                        comodel_name='olims.analysis_request',

    ),
    fields.Many2one(string='ParentAnalysisRequest',
                        comodel_name='olims.analysis_request',

    ),
    fields.Many2one(string='Priority',
                   comodel_name='olims.ar_priority',
                   required=False,

    ),
    TextField(
        string='ResultsInterpretation',
    ),
    fields.One2many(string='LabService',
                     comodel_name='olims.field_analysis_service',
                    inverse_name='ar_service_lab_id',
    ),
    fields.One2many(string='FieldService',
                     comodel_name='olims.field_analysis_service',
                    inverse_name='analysis_request_id',
    ),
    fields.Float(string='Discount',
                 compute='_ComputeServiceCalculation',
                 default=0.00
    ),
    fields.Float(string='Subtotal',
                 compute='_ComputeServiceCalculation',
                 default=0.00
    ),
    fields.Float(string='VAT',
                 compute='_ComputeServiceCalculation',
                 default=0.00
    ),
    fields.Float(string='Total',
                 compute='_ComputeServiceCalculation',
                 default=0.00
    ),
    fields.Selection(string='state',
                     selection=AR_STATES,
                     default='sample_registered',
                     select=True,
                     required=True, readonly=True,
                     copy=False, track_visibility='always'
    ),
    fields.Selection(string='result_option',
                     selection=(('general','General'),
                                ('sampling','Sampling')
                                ),
                     default='general',
    ),
    fields.One2many(string="Field_Manage_Result",
        comodel_name="olims.manage_analyses",
        inverse_name="manage_analysis_id"),
    fields.One2many(string="Lab_Manage_Result",
        comodel_name="olims.manage_analyses",
        inverse_name="lab_manage_analysis_id"),
    fields.One2many(string="AddAnalysis",
        comodel_name="olims.add_analysis",
        inverse_name="add_analysis_id")
)
schema_analysis = (fields.Many2one(string='Service',
                    comodel_name='olims.analysis_service',
                    relation='analysisservice_analysisrequest',
                    domain="[('PointOfCapture', '=', 'field'),('category', '=', Category)]"
    ),
    fields.Many2one(string='LabService',
                     comodel_name='olims.analysis_service',
                    relation='analysisservice_analysisrequest',
                    domain="[('PointOfCapture', '=', 'lab'),('category', '=', Category)]"
    ),
    StringField('CommercialID',
        compute='_ComputeFieldResults',
        widget=StringWidget(
            label=_("Commercial ID"),
            description=_("The service's commercial ID for accounting purposes")
        ),
    ),
    StringField('ProtocolID',
        compute='_ComputeFieldResults',
        widget=StringWidget(
            label=_("Protocol ID"),
            description=_("The service's analytical protocol ID")
        ),
    ),
    fields.Many2one(string='analysis_request_id',
        comodel_name='olims.analysis_request',
        ondelete='cascade'
    ),
    fields.Many2one(string='ar_service_lab_id',
        comodel_name='olims.analysis_request',
        ondelete='cascade'
    ),
    StringField(string="Error"),
    StringField(string="Min"),
    StringField(string="Max"),
    fields.Many2one(string='Category',
        comodel_name='olims.analysis_category'),
)

manage_result_schema = (
    StringField(string="Partition"),
    StringField(string="Result"),
    BooleanField('+-', default=False),
    DateTimeField('Capture'),
    DateTimeField('Due Date'),
    # fields.Many2one(string="Result",
    #     comodel_name="olims.result_option"),
    fields.Many2one(string="Instrument",
        comodel_name="olims.instrument"),
    fields.Many2one(string="Analyst",
        comodel_name="res.users",
        domain="[('groups_id', 'in', [14,22])]"),
    StringField('Specifications'),
    fields.Many2one(string='manage_analysis_id',
        comodel_name='olims.analysis_request',
        # domain="[('state', '=', 'sample_received')]",
        ondelete='cascade'
    ),
    fields.Many2one(string='lab_manage_analysis_id',
        comodel_name='olims.analysis_request',
        # domain="[('state', '=', 'sample_received')]",
        ondelete='cascade'
    ),
    fields.Many2one(string='Method',
        comodel_name='olims.method',
        ),
    fields.Many2one(string='Category',
        comodel_name='olims.analysis_category'),
    )

class AnalysisRequest(models.Model, BaseOLiMSModel): #(BaseFolder):
    _name = 'olims.analysis_request'
    _rec_name = "RequestID"

    def compute_analysisRequestId(self):
        for record in self:
            record.RequestID = 'R-0' + str(record.id)
    @api.multi
    def Compute_AnalysisSample(self):
        for record in self:
            if not record.Sample_id:
                sample = self.env["olims.sample"].search([('Analysis_Request', '=', record.id)])
                record.Sample = sample.SampleID
                record.Sample_id = sample.id
            else:
                record.Sample = record.Sample_id.SampleID

    @api.model
    def create(self, values):
        """Overwrite the create method of Odoo and create sample model data
           with fields SamplingDate and SampleType
        """
        data = []
        lab_result_list = []
        field_result_list = []
        analysis_object = super(AnalysisRequest, self).search([])
        if len(analysis_object) > 0:
            for ar_item in analysis_object[len(analysis_object)-1]:
                Partition = 'P-0'+ str(ar_item.id+1)+'-R-0'+str(ar_item.id+1)
        else:
            Partition = "P-01-R-01"
        for LabService in values.get('LabService'):
            Specification = ">"+str(LabService[2]['Min'])+", <"+str(LabService[2]['Max'])+", %"+str(LabService[2]['Error'])
            service_instance = self.env['olims.analysis_service'].search([('id', '=', LabService[2]['LabService'])])
            if service_instance._Method and service_instance.InstrumentEntryOfResults == False:
                LabService[2].update({'Method':service_instance._Method.id})
            elif service_instance.InstrumentEntryOfResults:
                LabService[2].update({'Method':None, 'Instrument': service_instance.Instrument})
            LabService[2].update({'Specifications':Specification,
                "Due Date": datetime.datetime.now(),
                'Partition':Partition})
            lab_result_list.append([0,0, LabService[2]])
        for FieldService in values.get('FieldService'):
            Specification = ">"+str(FieldService[2]['Min'])+", <"+str(FieldService[2]['Max'])+", %"+str(FieldService[2]['Error'])
            service_instance = self.env['olims.analysis_service'].search([('id', '=', FieldService[2]['Service'])])
            if service_instance._Method and service_instance.InstrumentEntryOfResults == False:
                FieldService[2].update({'Method':service_instance._Method.id})
            elif service_instance.InstrumentEntryOfResults:
                FieldService[2].update({'Method':None, 'Instrument': service_instance.Instrument})
            FieldService[2].update({'Specifications':Specification,
                "Due Date": datetime.datetime.now(),
                'Partition':Partition})

            field_result_list.append([0,0, FieldService[2]])
            data.append(FieldService)

        values.update({"Field_Manage_Result": field_result_list,
            "Lab_Manage_Result": lab_result_list})
        res = super(AnalysisRequest, self).create(values)
        
        smaple_vals_dict = {
                'SamplingDate':values.get('SamplingDate'),
                'SampleType':values.get('SampleType'),
                'Client': values.get('Client'),
                'Analysis_Request': res.id,
                'ClientReference': values.get('ClientReference'),
                'ClientSampleID': values.get('ClientSampleID'),
                'SamplePoint': values.get('SamplePoint'),
                'StorageLocation': values.get('StorageLocation'),
                'SamplingDeviation': values.get('SamplingDeviation'),
                'SampleCondition': values.get('SampleCondition'),
                }
        sample_object = self.env["olims.sample"]
        new_sample = sample_object.create(smaple_vals_dict)

        analysis_object = super(AnalysisRequest, self).search([('id', '=',res.id)])
        analysis_object.write({"Sample_id":new_sample.id})

        partition_values = {'State': res.state,
                            'analysis_request_id':res.id,
                            'Partition': 'P-0'+ str(res.id)+'-R-0'+str(res.id)
                            }
        ar_partition_object = self.env["olims.ar_partition"]
        ar_sample_partition_object = self.env["olims.ar_sample_partition"]
        ar_sample_partition_object.create(partition_values)
        ar_p = ar_partition_object.create(partition_values)
        ar_analysis_object = self.env['olims.ar_analysis']
        ar_service_lab_id = None
        for rec in data:
            if "LabService" in rec[2]:
                serv_temp = rec[2]['LabService']
            elif "Service" in rec[2]:
                serv_temp = rec[2]['Service']
            analyses_values = {
                               'Priority':values.get('Priority'),
                               'Partition': ar_p.id,
                               'analysis_request_id':res.id,
                               'Category': rec[2]['Category'],
                               'Services': serv_temp,
                               'Min': rec[2]['Min'],
                               'Max': rec[2]['Max'],
                               'Error': rec[2]['Error']
                               }
            ar_analysis_object.create(analyses_values)
        return res

    @api.multi
    def write(self, values):
        result_val_dict = {}
        if values.get("Analyses", None):
            for items in values.get("Analyses"):
                if items[0] == 0:
                    result_val_dict.update({
                            "Specifications":">"+str(items[2].get("Min", None))+", <"+str(items[2].get("Max", None))+", %"+str(items[2].get("Error", None)),
                            "Category": items[2].get("Category"),
                            'Due Date':datetime.datetime.now()
                            })
                    if items[2].get("Partition", None):
                        partition = self.env["olims.ar_partition"].search([("id", '=', items[2].get("Partition"))])
                        result_val_dict.update({"Partition": partition.Partition})
                    else:
                        result_val_dict.update({"Partition": 'P-0'+ str(self.id)+'-R-0'+str(self.id)})
                    if items[2].get("Services", None):
                        service = self.env["olims.analysis_service"].search([('id', '=', items[2].get("Services"))])
                        if service._Method and service.InstrumentEntryOfResults == False:
                            result_val_dict.update({'Method':service._Method.id})
                        elif service.InstrumentEntryOfResults:
                            result_val_dict.update({'Method':None, 'Instrument': service.Instrument})
                        if service.PointOfCapture == 'field':
                            result_val_dict.update({
                                'Service': items[2].get("Services"),
                                })
                            values.update({"Field_Manage_Result": [[0, False, result_val_dict]]})
                        else:
                            result_val_dict.update({
                                'LabService': items[2].get("Services"),
                                })
                            values.update({"Lab_Manage_Result": [[0, False, result_val_dict]]})
                if items[0] == 2:
                    pass
                if items[0] == 1:
                   pass
        res = super(AnalysisRequest, self).write(values)
        return res  

    @api.multi
    def publish_analysis_request(self):
        # self.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
        return self.env['report'].get_action(self, 'olims.report_analysis_request')

    def actionToBeSampled(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'to_be_sampled',
        }, context=context)
        return True

    def getSubtotalTotalPrice(self):
        """ Compute the price with VAT but no member discount"""
        return self.getSubtotal() + self.getSubtotalVATAmount()

    @api.onchange('LabService','FieldService')
    def _ComputeServiceCalculation(self):
        """
        It computes and returns the analysis service's discount amount without VAT, SubToatl and Total
        """
        for record in self:
            discount = 0.0
            vatamout = 0.0
            service_price = 0.0
            service_discount = 0.0
            service_subtotal = 0.0
            service_vat = 0.0
            service_total = 0.0
            if record.FieldService and record.LabService:
                for service in record.FieldService:

                    service_price = service.Service.Price

                    service_discount += service_price * 33.33 / 100

                    #compute subtotal
                    discount = service_price * 33.33 / 100
                    service_subtotal += float(service_price) - float(discount)

                    #compute VAT
                    service_vat += service.Service.VATAmount

                    service_total = service_subtotal + service_vat

                for service in record.LabService:

                    service_price = service.LabService.Price

                    service_discount += service_price * 33.33 / 100

                    #compute subtotal
                    discount = service_price * 33.33 / 100
                    service_subtotal += float(service_price) - float(discount)

                    #compute VAT
                    service_vat += service.LabService.VATAmount

                    service_total = service_subtotal + service_vat

                record.Discount = service_discount
                record.Subtotal = service_subtotal
                record.VAT = service_vat
                record.Total = service_total
            elif record.FieldService or record.LabService:
                if record.FieldService:
                    for service in record.FieldService:

                        service_price = service.Service.Price

                        service_discount += service_price * 33.33 / 100

                        #compute subtotal
                        discount = service_price * 33.33 / 100
                        service_subtotal += float(service_price) - float(discount)

                        #compute VAT
                        service_vat += service.Service.VATAmount

                        service_total = service_subtotal + service_vat

                    record.Discount = service_discount
                    record.Subtotal = service_subtotal
                    record.VAT = service_vat
                    record.Total = service_total
                if record.LabService:
                    for service in record.LabService:
                        service_price = service.LabService.Price

                        service_discount += service_price * 33.33 / 100

                        #compute subtotal
                        discount = service_price * 33.33 / 100
                        service_subtotal += float(service_price) - float(discount)

                        #compute VAT
                        service_vat += service.LabService.VATAmount

                        service_total = service_subtotal + service_vat

                    record.Discount = service_discount
                    record.Subtotal = service_subtotal
                    record.VAT = service_vat
                    record.Total = service_total

    def getTotalPrice(self):
        """
        It gets the discounted price from analyses and profiles to obtain the total value with the VAT
        and the discount applied
        :return: the analysis request's total price including the VATs and discounts
        """
        for record in self:
            record.Total = record.Subtotal + record.VAT

    def isInvalid(self,cr,uid,ids,context=None):
        """ return if the Analysis Request has been invalidated
        """
        return self.write(cr, uid, ids, {
            'state': 'invalid',
        }, context=context)
        return True

    def workflow_script_receive(self,cr,uid,ids,context=None):
        analysis_dict = {}
        add_analysis_object = self.pool.get('olims.add_analysis')
        analysis_request_obj = self.pool.get('olims.analysis_request').browse(cr,uid,ids,context)
        manage_result_object = self.pool.get('olims.manage_analyses').search(cr,uid,['|',
            ('manage_analysis_id', '=', ids),('lab_manage_analysis_id', '=', ids)],context)
        for items in self.pool.get('olims.manage_analyses').browse(cr,uid,manage_result_object,context):
            analysis_dict.update({
                'category':items.Category.id,
                'client': analysis_request_obj.Client.id,
                'order':analysis_request_obj.ClientOrderNumber,
                'priority':analysis_request_obj.Priority.id,
                'due_date':analysis_request_obj.DateDue,
                'received_date':datetime.datetime.now()
                })
            if items.Service:
                analysis_dict.update({'analysis':items.Service.id })
            if items.LabService:
                analysis_dict.update({'analysis':items.LabService.id })
            self.write(cr, uid, ids, {'AddAnalysis': [[0,0, analysis_dict]]
                }, context=context)
        datereceived = datetime.datetime.now()
        self.write(cr, uid, ids, {
            'state': 'sample_received', 'DateReceived' : datereceived,
        }, context=context)
        return True

    def workflow_script_preserve(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'preserved',
        }, context=context)
        return True

    def workflow_script_sample(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'sampled',
        }, context=context)

        return True

    def workflow_script_to_be_preserved(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'to_be_preserved',
        }, context=context)
        return True

    def workflow_script_sample_due(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'sample_due', 'DateDue':datetime.datetime.now()
        }, context=context)
        return True

    def workflow_script_to_be_verified(self,cr,uid,ids,context=None):
        self.write(cr, uid, ids, {
            'state': 'to_be_verified',
        }, context=context)
        return True

    def workflow_script_verify(self):
        self.write({
            'state': 'verified',
        })
        return True

    def workflow_script_publish(self):
        datepublished = datetime.datetime.now()
        self.write({
            'state': 'published', 'DatePublished' : datepublished
        })
        return True


class FieldAnalysisService(models.Model, BaseOLiMSModel):
    _name = 'olims.field_analysis_service'

    @api.onchange('Service','LabService')
    def _ComputeFieldResults(self):
        for item in self:
            if item.Service:
                item.CommercialID = item.Service.CommercialID
                item.ProtocolID  = item.Service.ProtocolID
            if item.LabService:
                item.CommercialID = item.LabService.CommercialID
                item.ProtocolID  = item.LabService.ProtocolID

class ManageAnalyses(models.Model, BaseOLiMSModel):
    _inherit = 'olims.field_analysis_service'
    _name = 'olims.manage_analyses'


AnalysisRequest.initialze(schema)
FieldAnalysisService.initialze(schema_analysis)
ManageAnalyses.initialze(manage_result_schema)

