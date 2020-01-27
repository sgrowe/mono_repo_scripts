from pathlib import Path
from collections import Counter
from lxml import etree
import operator
import json
import csv


#
# CUSTOMISE THIS VARIABLES FOR YOUR PROJECT
#


# Path to the root of your repo
mono_repo = Path.home().joinpath('repo_path')


def mono_repo_folders():
    for x in mono_repo.iterdir():
        if x.is_dir():
            yield x


def main():
    js_package_counts = Counter()
    js_projects_count = 0

    java_package_counts = Counter()
    java_projects_count = 0

    for dir in mono_repo_folders():
        package_json = dir.joinpath('package.json')
        pom_xml = dir.joinpath('pom.xml')


        if package_json.exists():
            js_projects_count += 1

            with package_json.open() as f:
                packages = json.load(f)

            js_package_counts.update(packages.get('dependencies', {}).keys())
            js_package_counts.update(packages.get('devDependencies', {}).keys())

        if pom_xml.exists():
            java_projects_count += 1

            with pom_xml.open() as f:
                deps = etree.parse(f)
            dep_names = deps.xpath('//m:dependencies/m:dependency/m:artifactId/text()', namespaces={'m': 'http://maven.apache.org/POM/4.0.0'})
            java_package_counts.update(dep_names)

    print_results('JS', js_package_counts, js_projects_count)

    print_results('Java', java_package_counts, java_projects_count)


def print_results(lang, package_counts, projects_count, format='csv'):
    if format == 'csv':
        with open('out.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['Dependency', 'Number of projects using it'])
            for dep, count in sorted(package_counts.items(), key=lambda item: item[1], reverse=True):
                writer.writerow([dep, count])
    else:
        print('Number of', lang, 'projects:', projects_count)
        print('Total dependencies count:', len(package_counts))
        print()

        left_col_width = 50

        print('Dependency'.ljust(left_col_width), 'Number of projects using it')
        for dep, count in sorted(package_counts.items(), key=lambda item: item[1], reverse=True):
            print(dep.ljust(left_col_width), count)

        print()


if __name__ == '__main__':
    main()
