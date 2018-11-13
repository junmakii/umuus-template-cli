#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A package.

umuus-template-cli
==================

Installation
------------

    $ pip install umuus_template_cli

Example
-------

    $ umuus_template_cli

    >>> import umuus_template_cli

Authors
-------

- Jun Makii <junmakii@gmail.com>

License
-------

GPLv3 <https://www.gnu.org/licenses/>

"""
import os
import json
import sys
import re
import jinja2
import umuus_dict_util
import argparse
import addict
import functools
import yaml
import glob
__version__ = '0.1'
__url__ = 'https://github.com/junmakii/umuus-template-cli'
__author__ = 'Jun Makii'
__author_email__ = 'junmakii@gmail.com'
__keywords__ = []
__license__ = 'GPLv3'
__scripts__ = []
__install_requires__ = [
    'PyYAML',
    'jinja2',
    'addict',
    'git://github.com/junmakii/umuus_dict_util.git#egg=umuus_dict_util',
]
__classifiers__ = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Natural Language :: English',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
]
__entry_points__ = {'console_scripts': ['umuus_template_cli = umuus_template_cli:main']}


def parse_header(data):
    return (
        lambda matches:
        dict(content=matches[0][2],
             headers=yaml.safe_load(matches[0][0]))
        if matches
        else dict(content=data,
                  headers={})
    )(re.findall(r'^---\n((.|\n)*?)\n---\n((.|\n)+)', data, re.MULTILINE))


def parse_args(args=[]):  # type: (dict, dict)
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output')
    parser.add_argument('-i', '--input')
    parser.add_argument('-j', '--json', default='{}')
    parser.add_argument('-H', '--header', action='store_true')
    parser.add_argument('-c', '--config', action='append', default=[])
    parser.add_argument('-t', '--target')
    options, unknown_args = parser.parse_known_args(args)
    unknown_args = functools.reduce(
        lambda a, b: a + b,
        [[re.sub('^--ctx\.', '', key), value] for key, value in zip(unknown_args[0:None:2], unknown_args[1:None:2])] or [], [])
    options = vars(options)
    options['target_isfile'] = os.path.isfile(options['target'])
    if os.path.isfile(options['target']):
        options['target_dirname'] = os.path.dirname(options['target'])
        options['target'] = [options['target']]
    else:
        options['target_dirname'] = options['target']
        options['target'] = [os.path.join(options['target'], file)
                             for file in os.listdir(options['target'])]
    options['config'] = functools.reduce(
        lambda a, b: dict(a, **b),
        map(lambda _: json.load(open(_)), [
            glob.glob(_ + '/*.json')
            for _ in options['config']]), []) or {}
    context = umuus_dict_util.parse_args(unknown_args)
    return dict(
        options,
        context={
            key: value
            for key, value in (
                    list(context.items())
                    + list(options['config'].items())
            )})


def main(argv=[]):
    args = (argv and argv or sys.argv)
    options = addict.Dict(parse_args(args[1:]))
    options.template_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([options.target_dirname]))
    for target in options.target:
        header = parse_header(open(target).read())
        header_context = header['headers']
        content = header['content']
        options.template = options.template_env.from_string(content)
        options.content = options.template.render(
            **functools.reduce(lambda a, b: dict(a, **b),
                               [globals(), header_context, options.context]))
        if options.target_isfile:
            if options.output:
                open(options.output, 'w').write(options.content)
            else:
                print(options.content)
        else:
            options.dest = os.path.join(options.output, target[len(options.target_dirname) + 1:])
            not os.path.exists(os.path.dirname(options.dest)) and os.makedirs(os.path.dirname(options.dest))
            open(options.dest, 'w').write(options.content)
    return 0


if __name__ == '__main__':
    main(sys.argv)
