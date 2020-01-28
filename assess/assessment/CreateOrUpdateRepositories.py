import requests
import json

from django.core.management.base import BaseCommand

from victrassessment import models as vModels


def api_request_generator(number_of_repos=100, language='python', sort_by='stars', sort_order='desc', per_page=100):
    base_url = 'https://api.github.com/search/'
    type_of_search = 'repositories'
    query_string = '?q=language:{}&sort={}&order={}&per_page={}&page='
    page_count = 1
    while page_count * per_page <= number_of_repos:
        yield base_url + type_of_search + query_string.format(
            language,
            sort_by,
            sort_order,
            number_of_repos
        )
        page_count +=1


def build_response_dict(options):
    response_json = {}
    for request_string in api_request_generator(**options):
        response = requests.get(request_string)
        if response.ok:
            response_json.update(json.loads(response._content))

    return response_json


class Command(BaseCommand, ReTransCommonArguments):

    def add_arguments(self, parser):
        parser.add_argument(
            '--repos',
            action='store',
            dest='number_of_repos',
            default=False,
            help='Number of repositories to retrieve. Default is 100',
        )
        parser.add_argument(
            '--language',
            action='store',
            dest='language',
            default=False,
            help='Which language to search for. Default is Python',
        )
        parser.add_argument(
            '--sort_by',
            action='store',
            dest='sort_by',
            default=False,
            help='Which feature to sort by. Default is number of stars.',
        )
        parser.add_argument(
            '--sort_order',
            action='store',
            dest='language',
            default=False,
            help='Which order to display results. Default is desc',
        )


    def handle(self, *args, **options):
        request_json = build_response_dict()

        for item in request_json['items']:
            default_values = {
                'project_name': item['name'],
                'project_url': item['url'],
                'project_creation_date': item['created_at'],
                'last_pushed': item['pushed'],
                'description': item['description'],
                'number_of_stars': item['stargazers_count'],
            }

            repo, _ = vModels.PopularGithubRepositories.objects.update_or_create(
                repository_id=83222441,
                defaults=default_values,
            )
