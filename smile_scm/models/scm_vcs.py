# -*- coding: utf-8 -*-

from odoo import api, fields, models

from ..tools import call


class VersionControlSystem(models.Model):
    _name = 'scm.vcs'
    _description = 'Version Control System'

    name = fields.Char(required=True)
    cmd = fields.Char('Command', size=3, required=True)
    cmd_clone = fields.Char('Clone', required=True)
    cmd_pull = fields.Char('Pull', required=True)
    cmd_list = fields.Char('List branches', required=False)
    default_branch = fields.Char('Default branch')

    _sql_constraints = [
        ('unique_cmd', 'UNIQUE(cmd)', 'VCS must be unique'),
    ]

    @api.multi
    def clone(self, directory, branch, url):
        self.ensure_one()
        localdict = {'url': url, 'branch': branch or self.default_branch}
        cmd_clone = self.cmd_clone % localdict
        cmd = cmd_clone.split(' ')
        cmd.append(directory)
        call(cmd)
        return True

    @api.multi
    def pull(self, directory):
        self.ensure_one()
        call(self.cmd_pull, directory)
        return True

    @api.multi
    def list(self, directory, url):
        self.ensure_one()
        cmd = self.cmd_list % {'url': url}
        result = call(cmd, directory).split('\n')
        if '' in result:
            result.remove('')
        return result
