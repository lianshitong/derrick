#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import os

from derrick.core.detector_report import DetectorReport
from derrick.core.rigging import Rigging
from derrick.detectors.image.node import NodeVersionDetector
from derrick.detectors.general.image_repo import ImageRepoDetector

PLATFORM = "NodeJs"


class NodejsRigging(Rigging):
    def detect(self, context):
        """
        :param context:
        :return: handled(bool),platform(string)
        """
        workspace = context.get("WORKSPACE")
        package_json_file = os.path.join(workspace, "package.json")
        if os.path.exists(package_json_file) is True:
            return True, PLATFORM
        return False, None

    def compile(self, context):
        dr = DetectorReport()
        docker_node = dr.create_node("Dockerfile.j2")
        docker_node.register_detector(NodeVersionDetector())

        docker_compose_node = dr.create_node("docker-compose.yml.j2")
        docker_compose_node.register_detector(ImageRepoDetector())

        jenkins_file_node = dr.create_node("Jenkinsfile.j2")
        jenkins_file_node.register_detector(ImageRepoDetector())

        return dr.generate_report()
