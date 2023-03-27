#!/usr/bin/env python3
"""
(C) 2021 Genentech. All rights reserved.

Top-level invoke task.
"""

import invoke

import cdd_chem_subtasks.cruft as cruft
import cdd_chem_subtasks.docs as docs
import cdd_chem_subtasks.lint as lint
import cdd_chem_subtasks.package as package
import cdd_chem_subtasks.test as test

namespace = invoke.Collection(cruft, docs, package, lint, test)
