# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

from decisionengine.framework.tests import ModuleProgramOptions as opts


def test_help():
    opts.Help("SourceNOP").test()
    opts.Help("TransformNOP").test()
    opts.Help("PublisherNOP").test()
    opts.Help("SourceWithSampleConfigNOP").test(has_sample_config=True)


def test_config_templates():
    opts.ConfigTemplate("SourceNOP").test()
    opts.ConfigTemplate("TransformNOP").test()
    opts.ConfigTemplate("PublisherNOP").test()
    opts.ConfigTemplate("SupportsConfigPublisher").test(has_comments=True)


def test_module_alias():
    opts.DescribeAlias("SourceAlias", original="SourceWithSampleConfigNOP").test()


def test_descriptions():
    opts.Describe("SourceNOP").test(produces="foo")
    opts.Describe("TransformNOP").test(consumes="foo", produces="bar")
    opts.Describe("PublisherNOP").test(consumes="bar")


def test_acquire_for_sources():
    acquire_with_config = opts.AcquireWithConfig("SourceWithSampleConfigNOP")
    acquire_with_config.test(rb"{}", expected_stderr="Could not locate 'sources' configuration block")
    acquire_with_config.test(rb"{ sources: {} }", expected_stderr="No configuration in.*is supported")

    jsonnet_variable = b"local spec = 'decisionengine.framework.tests.SourceWithSampleConfigNOP';"
    acquire_with_config.test(
        jsonnet_variable + rb"{ sources: { source1: { module: spec }, source2: { module: spec }} }",
        expected_stderr="Located more than one.*Please choose one of",
    )
    acquire_with_config.test(
        jsonnet_variable + rb"{ sources: { source1: { module: spec } } }",
        expected_stderr="Configuration.*does not contain a 'parameters' table",
    )
    acquire_with_config.test(
        jsonnet_variable
        + rb"{ sources: { src: { module: spec, parameters: { channel_name: 'test', multiplier: 2 } } } }"
    )

    opts.AcquireWithSampleConfig("SourceWithSampleConfigNOP").test()
