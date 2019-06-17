# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools.sql import drop_view_if_exists

import datetime

class RegistroCompras(models.Model):
    _name = "registro.compras"
    _description = "Registro de Compras"
    _auto = False

    id = fields.Char()
    date_invoice = fields.Date()
    date_due = fields.Date()
    tipo_cp = fields.Char()
    serie = fields.Char()
    number = fields.Char()
    tipo_persona = fields.Char()
    tipo_doc = fields.Char()
    vat = fields.Char()
    vendor_display_name = fields.Char()
    amount_untaxed = fields.Float()
    exempted = fields.Float()
    no_vat = fields.Float()
    isc = fields.Float()
    amount_tax = fields.Float()
    others = fields.Float()
    amount_total = fields.Float()
    type = fields.Char(size=100)
    state = fields.Char(size=100)
    account_date = fields.Date()
    account_period = fields.Char(size=8)
    correlativo = fields.Char(size=9)
    currency_name = fields.Char(size=3)
    rate = fields.Float()
    cuo = fields.Char()
    
    #El campo texto va al final y contiene la línea del PLE
    texto = fields.Char()
    
    @api.model_cr
    def init(self):
       drop_view_if_exists(self.env.cr,self._table)
       self._cr.execute('''
             create or replace view 
             registro_compras as (
                    
                    select ai.id, 
                           ai.date_invoice, 
                           ai.date_due, 
                           substr(ai.x_studio_tipo_comprobante_pago,1,2) tipo_cp,                       
                           case when position('-' in ai.number) = 0 then '' 
                                else substr(ai.number, 1, position('-' in ai.number)-1) 
                           end serie,
                           case when position('-' in ai.number) = 0 then ai.number 
                                else substr(ai.number, position('-' in ai.number)+1) 
                           end number,
                           substr(p.x_studio_tipo_persona,1,2) tipo_persona,
                           substr(p.x_studio_tipo_documento_identidad,1,1) tipo_doc,
                           p.vat, 
                           ai.vendor_display_name, 
                           ai.amount_untaxed_signed amount_untaxed,
                           0 exempted,
                           0 no_vat,
                           0 isc,                      
                           (ai.amount_total_company_signed - ai.amount_untaxed_signed) amount_tax, 
                           0 others,
                           ai.amount_total_company_signed amount_total,
                           ai.type,
                           ai.state,
                           ai.date account_date,
                           concat(	
                               extract(year from ai.date),
                               right(concat('0',extract(month from ai.date)),2),
                               '00'
                            ) account_period,
                           concat('M',
                                  right(concat('00000000',aml.id), 8)       
                                 ) correlativo,
                           c.name currency_name,
                           case when c.name = 'USD' then 1
                                else r.rate
                           end rate,
                           ai.move_id cuo,

                           trim(
                               concat_ws('|',
                                   concat(	
                                       extract(year from ai.date),
                                       right(concat('0',extract(month from ai.date)),2),
                                       '00'
                                    ),
                                   ai.move_id,
                                   concat(
                                       'M',
                                       right(concat('00000000',aml.id), 8)       
                                    ),
                                   to_char(ai.date_invoice,'DD/MM/YYYY'),
                                   to_char(ai.date_due,'DD/MM/YYYY'),
                                   substr(ai.x_studio_tipo_comprobante_pago,1,2),
                                   case when position('-' in ai.number) = 0 then '' 
                                        else substr(ai.number, 1, position('-' in ai.number)-1) 
                                   end,
                                   '',
                                   case when position('-' in ai.number) = 0 then ai.number 
                                        else substr(ai.number, position('-' in ai.number)+1) 
                                   end,
                                   '',
                                   substr(p.x_studio_tipo_documento_identidad,1,1),
                                   p.vat,
                                   ai.vendor_display_name,
                                   ai.amount_untaxed_signed,
                                   (ai.amount_total_company_signed - ai.amount_untaxed_signed),
                                   0,
                                   0,
                                   0,
                                   0,
                                   0,
                                   0,
                                   0,
                                   ai.amount_total_company_signed,
                                   c.name,
                                   to_char(coalesce(r.rate,1),'9D999'),
                                   '',
                                   '',
                                   '',
                                   '',
                                   '',
                                   coalesce(to_char(ai.x_studio_fecha_emisin_detraccin,'DD/MM/YYYY'),''),
                                   coalesce(ai.x_studio_nro_constancia_detraccin_1,''),
                                   '',
                                   trim(both '0' from coalesce(substr(ai.x_studio_clasificacin_de_bienes_y_servicios,1,2),'')),
                                   '',
                                   '',
                                   '',
                                   '',
                                   '',
                                   '',
                                   1,
                                   '',
                                   '',
                                   ''
                               )
                           ) as texto

                    from account_invoice ai
                         inner join (account_invoice_line ail 
                                         inner join account_move_line aml
                                             on (ail.account_id = aml.account_id)
                                    )
                             on (ai.id = ail.invoice_id and ai.move_id = aml.move_id)
                         inner join res_partner p 
                             on (ai.partner_id = p.id)
                         inner join res_currency c 
                             on (ai.currency_id = c.id)
                         left join res_currency_rate r 
                             on (ai.currency_id = r.currency_id and ai.date_invoice = r.name)
                    where ai.type = 'in_invoice' 
                      and ai.state not in ('draft')                      
                      and substr(ai.x_studio_tipo_comprobante_pago,1,2) not in ('91','97','98')

                    UNION ALL
                    select he.id,
                           he.x_studio_fecha_factura, 
                           null, 
                           substr(he.x_studio_tipo_comprobante_pago_1,1,2) tipo_cp,                       
                           case when position('-' in he.reference) = 0 then '' 
                                else substr(he.reference, 1, position('-' in he.reference)-1) 
                           end serie,
                           case when position('-' in he.reference) = 0 then he.reference 
                                else substr(he.reference, position('-' in he.reference)+1) 
                           end number,
                           substr(p.x_studio_tipo_persona,1,2) tipo_persona,
                           substr(p.x_studio_tipo_documento_identidad,1,1) tipo_doc,
                           p.vat, 
                           p.name, 
                           0 amount_untaxed,
                           0 exempted,
                           he.untaxed_amount no_vat,
                           0 isc,                      
                           0 amount_tax, 
                           0 others,
                           he.total_amount amount_total,
                           'expense',
                           he.state,
                           he.date account_date,
                           concat(    
                               extract(year from he.date),
                               right(concat('0',extract(month from he.date)),2),
                               '00'
                            ) account_period,
                           concat('M',
                                  right(concat('00000000',aml.id), 8)       
                                 ) correlativo,
                           c.name currency_name,
                           case when c.name = 'USD' then 1
                                else r.rate
                           end rate,
                           hes.account_move_id cuo,

                           trim(
                               concat_ws('|',
                                   concat(    
                                       extract(year from he.date),
                                       right(concat('0',extract(month from he.date)),2),
                                       '00'
                                    ),
                                   hes.account_move_id,
                                   concat('M',
                                          right(concat('00000000',aml.id), 8)       
                                         ),
                                   to_char(he.x_studio_fecha_factura,'DD/MM/YYYY'),
                                   '',
                                   substr(he.x_studio_tipo_comprobante_pago_1,1,2),
                                   case when position('-' in he.reference) = 0 then '' 
                                        else substr(he.reference, 1, position('-' in he.reference)-1) 
                                   end,
                                   '',
                                   case when position('-' in he.reference) = 0 then he.reference 
                                        else substr(he.reference, position('-' in he.reference)+1) 
                                   end,
                                   '',
                                   substr(p.x_studio_tipo_documento_identidad,1,1),
                                   p.vat,
                                   p.name,
                                   0,
                                   0,
                                   0,
                                   0,
                                   0,
                                   0,
                                   he.untaxed_amount,
                                   0,
                                   0,
                                   he.total_amount,
                                   c.name,
                                   to_char(coalesce(r.rate,1),'9D999'),
                                   '',
                                   '',
                                   '',
                                   '',
                                   '',
                                   coalesce(to_char(he.x_studio_fecha_constancia_detraccin,'DD/MM/YYYY'),''),
                                   coalesce(he.x_studio_nro_constancia_detraccin,''),
                                   '',
                                   trim(both '0' from coalesce(substr(he.x_studio_clasificacin_de_bienes_y_servicios,1,2),'')),
                                   '',
                                   '',
                                   '',
                                   '',
                                   '',
                                   '',
                                   1,
                                   '',
                                   '',
                                   ''
                               )
                           ) as texto

                    from hr_expense he
                         inner join (hr_expense_sheet hes 
                                         inner join account_move_line aml 
                                             on (hes.account_move_id = aml.move_id)
                                    )
                             on (he.sheet_id = hes.id and he.account_id = aml.account_id)
                         inner join res_partner p 
                             on (he.x_studio_proveedor = p.id)
                         inner join res_currency c 
                             on (he.currency_id = c.id)
                         left join res_currency_rate r 
                             on (he.currency_id = r.currency_id and he.x_studio_fecha_factura = r.name)                         
                    where he.state not in ('draft')                      
                      and substr(he.x_studio_tipo_comprobante_pago_1,1,2) not in ('91','97','98')

             )
        ''')
