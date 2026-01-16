import unittest
import lxml.html

from natcap.invest.carbon import MODEL_SPEC

from invest_reports import jinja_env

TEMPLATE = jinja_env.get_template('carbon.html')


def _get_render_args(model_spec):
    timestamp = '1970-01-01'
    args_dict = {'suffix': 'test'}
    img_src = 'bAse64eNcoDEdIMagE'
    output_stats_table = '<table class="test__output-stats-table"></table>'
    input_stats_table = '<table class="test__input-stats-table"></table>'
    stats_table_note = 'This is a test!'
    inputs_caption = ['input.tif:Input map.']
    outputs_caption = ['results.tif:Results map.']
    intermediate_raster_sections = []
    raster_group_caption = 'This is another test!'
    agg_results_table = '<table class="test__agg-results-table"></table>'

    return {
        'report_script': __file__,
        'model_id': model_spec.model_id,
        'model_name': model_spec.model_title,
        'userguide_page': model_spec.userguide,
        'timestamp': timestamp,
        'args_dict': args_dict,
        'agg_results_table': agg_results_table,
        'inputs_img_src': img_src,
        'inputs_caption': inputs_caption,
        'outputs_img_src': img_src,
        'outputs_caption': outputs_caption,
        'intermediate_raster_sections': intermediate_raster_sections,
        'raster_group_caption': raster_group_caption,
        'output_raster_stats_table': output_stats_table,
        'input_raster_stats_table': input_stats_table,
        'stats_table_note': stats_table_note,
        'model_spec_outputs': model_spec.outputs,
    }


def _mock_intermediate_output_sections(num_sections):
    return [
        {
            'heading': f'Intermediate Outputs {i + 1}',
            'img_src': 'bAse64eNcoDEdIMagE',
            'caption': ['map1.tif:Map of baseline-scenario carbon values.',
                        'map2.tif:Map of alternate-scenario carbon values.'],
        } for i in range(num_sections)
    ]


class CarbonTemplateTests(unittest.TestCase):
    """Unit tests for Carbon template."""

    def test_render_without_alt_scenario(self):
        """Make sure the template renders without error."""

        render_args = _get_render_args(MODEL_SPEC)
        render_args['intermediate_raster_sections'] = (
            _mock_intermediate_output_sections(1))

        html = TEMPLATE.render(render_args)
        root = lxml.html.document_fromstring(html)

        sections = root.find_class('accordion-section')
        # 7 default sections plus 1 section for intermediate outputs.
        self.assertEqual(len(sections), 8)

        h1 = root.find('.//h1')
        self.assertEqual(h1.text, f'InVEST Results: {MODEL_SPEC.model_title}')

    def test_render_with_alt_scenario(self):
        """Make sure the template renders without error."""

        render_args = _get_render_args(MODEL_SPEC)
        render_args['intermediate_raster_sections'] = (
            _mock_intermediate_output_sections(4))

        html = TEMPLATE.render(render_args)
        root = lxml.html.document_fromstring(html)

        sections = root.find_class('accordion-section')
        # 7 default sections plus 4 sections for intermediate outputs.
        self.assertEqual(len(sections), 11)

        h1 = root.find('.//h1')
        self.assertEqual(h1.text, f'InVEST Results: {MODEL_SPEC.model_title}')
