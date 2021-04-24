#!/usr/bin/python
 -*- encoding: utf-8; py-indent-offset: 4 -*-

# Rules for configuring parameters of check adsl_line

from cmk.gui.i18n import _

from cmk.gui.valuespec import (
    Dictionary,
    Integer,
    TextAscii,
    Tuple,
)

from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    rulespec_registry,
    RulespecGroupCheckParametersNetworking,
)

def _item_valuespec_adsl_line():
    return TextAscii(
            title=_("ADSL interface"),
            help=_('Number of the ADSL interface'),
            )

def _parameter_valuespec_adsl_line():
    return Dictionary(
            elements=[
           ('upstream_params',
               Tuple(
                    title='Upstream Rate',
                    help = _('Minimum Upstream Rate'),
                    elements = [
                        Integer(title=_('Warning below'),unit='Mbit/s',default_value='15'),
                        Integer(title=_('Critical below'),unit='Mbit/s',default_value='10'),
                        ] ) ),
           ('downstream_params',
               Tuple(
                    title='Downstream Rate',
                    help = _('Minimum Downstream Rate'),
                    elements = [
                        Integer(title=_('Warning below'),unit='Mbit/s',default_value='50'),
                        Integer(title=_('Critical below'),unit='Mbit/s',default_value='10'),
                        ] ) ),
            ('snr_margin_params',
                Tuple(
                    title='SNR Margin',
                    help = _('Minimum SNR Margin'),
                    elements = [
                        Integer(title=_('Warning below'),unit='dB',default_value='10'),
                        Integer(title=_('Critical below'),unit='dB',default_value='5'),
                        ] ) ),
            ('attenuation_params',
                Tuple(
                    title='Attenuation',
                    help = _('Maximum Attenuation'),
                    elements = [
                        Integer(title=_('Warning above'),unit='dB',default_value='30'),
                        Integer(title=_('Critical above'),unit='dB',default_value='45'),
                        ] ) ),
            ]
        )

rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name="adsl_line",
        group=RulespecGroupCheckParametersNetworking,
        match_type="dict",
        item_spec=_item_valuespec_adsl_line,
        parameter_valuespec=_parameter_valuespec_adsl_line,
        title=lambda: _("Metrics of ADSL line"),
    ))
