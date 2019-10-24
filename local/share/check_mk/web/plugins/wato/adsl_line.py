#!/usr/bin/python
# -*- encoding: utf-8; py-indent-offset: 4 -*-

# Rules for configuring parameters of check adsl_line

register_check_parameters(
    subgroup_networking,
        'adsl_line',
        _('ADSL Line'),
        Dictionary(
            title = _('ADSL Line'),
            help = _('Check the Status of ADSL Lines'),
            elements = [
                ('upstream_params', Tuple(
                    title='Upstream Rate',
                    help = _('Minimum Upstream Rate'),
                    elements = [
                        Integer(title=_('Warning at'),unit='Mbit/s',default_value='50'),
                        Integer(title=_('Critical at'),unit='Mbit/s',default_value='30'),
                        ] ) ),
                ('downstream_params', Tuple(
                    title='Downstream Rate',
                    help = _('Minimum Downstream Rate'),
                    elements = [
                        Integer(title=_('Warning at'),unit='Mbit/s',default_value='50'),
                        Integer(title=_('Critical at'),unit='Mbit/s',default_value='30'),
                        ] ) ),
                ('snr_margin_params', Tuple(
                    title='SNR Margin',
                    help = _('Minimum SNR Margin'),
                    elements = [
                        Integer(title=_('Warning at'),unit='dB',default_value='8'),
                        Integer(title=_('Critical at'),unit='dB',default_value='5'),
                        ] ) ),
                ('attenuation_params', Tuple(
                    title='Attenuation',
                    help = _('Maximum Attenuation'),
                    elements = [
                        Integer(title=_('Warning at'),unit='dB',default_value='40'),
                        Integer(title=_('Critical at'),unit='dB',default_value='50'),
                        ] ) ),
            ]
        ),
        TextAscii(
            title = _("ADSL Line"),
            help = _("Specify the Interface Number of ADSL Line. "),
            allow_empty = False
            ),
        'dict'
    )



