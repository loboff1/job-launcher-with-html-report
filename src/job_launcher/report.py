import json
import logging
from os import path
from typing import Dict
from jinja2 import Environment, PackageLoader, select_autoescape

import job_launcher

log = logging.getLogger(__name__)

JSON_REPORT = 'job_launcher_result.json'


def dump_json_report(data: Dict, output: str):
    with open(path.join(output, JSON_REPORT), 'w') as f:
        json.dump(data, f, indent=2)


class Reporter:
    HTML_REPORT = 'job_launcher_result.html'

    def __init__(self, output: str):
        self.html_result = None
        self.json_report_file = path.join(output, JSON_REPORT)
        self.html_report_file = path.join(output, self.HTML_REPORT)

    def generate(self):
        environment = Environment(
            loader=PackageLoader(job_launcher.__name__, 'resources/templates'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        template = environment.get_template('job_launcher_templ.html')

        log.info('Start report generation')
        json_report = self._load_json_report()
        json_server = json_report.get('server'),
        json_results = json_report.get('results')
        message = self._get_message(json_server, json_results)
        log.info(message)
        log.info('Finish report generation')
        html_result = template.render(server=json_server, results=json_results)
        self.dump_html(html_result)

    def dump_html(self, html_result):
        with open('output/job_launcher_result.html', 'w') as f:
            f.write(html_result)

    def _load_json_report(self):
        with open(self.json_report_file) as f:
            return json.load(f)

    def _get_message(self, server, results=None):
        results = results or []
        message = [f'Jenkins server: {server}']
        for result in results:
            message.append(f'name: {result.get("name")}')
            message.append(f'status: {result.get("status")}')
            message.append(f'timestamp: {result.get("result", {}).get("timestamp") or "-"}')
            message.append(f'number: {result.get("result", {}).get("number") or "-"}')
            message.append('')
        return '\n'.join(message)
