from odoo import models, fields, api, exceptions

class MasterRuangan(models.Model):
    _name = 'master.ruangan'
    _description = 'Master Ruangan'

    name = fields.Char(string='Nama Ruangan', required=True)
    tipe_ruangan = fields.Selection([
        ('kecil', 'Meeting Room Kecil'),
        ('besar', 'Meeting Room Besar'),
        ('aula', 'Aula')
    ], string='Tipe Ruangan', required=True)
    lokasi_ruangan = fields.Selection([
        ('1A', '1A'),
        ('1B', '1B'),
        ('1C', '1C'),
        ('2A', '2A'),
        ('2B', '2B'),
        ('2C', '2C')
    ], string='Lokasi Ruangan', required=True)
    foto_ruangan = fields.Binary(string='Foto Ruangan', required=True)
    kapasitas_ruangan = fields.Integer(string='Kapasitas Ruangan', required=True)
    keterangan = fields.Text(string='Keterangan')


class PemesananRuangan(models.Model):
    _name = 'pemesanan.ruangan'
    _description = 'Pemesanan Ruangan'

    nomor_pemesanan = fields.Char(string='Nomor Pemesanan', required=True, unique=True)
    ruangan_id = fields.Many2one('master.ruangan', string='Ruangan', required=True)
    nama_pemesanan = fields.Char(string='Nama Pemesanan', required=True)
    tanggal_pemesanan = fields.Date(string='Tanggal Pemesanan', required=True)
    status_pemesanan = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'On Going'),
        ('done', 'Done')
    ], string='Status Pemesanan', default='draft')
    catatan_pemesanan = fields.Text(string='Catatan Pemesanan')

    @api.constrains('ruangan_id', 'tanggal_pemesanan')
    def check_ruangan_availability(self):
        for record in self:
            existing_reservation = self.search([
                ('ruangan_id', '=', record.ruangan_id.id),
                ('tanggal_pemesanan', '=', record.tanggal_pemesanan),
                ('id', '!=', record.id)
            ])
            if existing_reservation:
                raise exceptions.ValidationError('Ruangan sudah dipesan pada tanggal ini.')

    @api.constrains('nama_pemesanan')
    def check_nama_pemesanan(self):
        for record in self:
            existing_reservation = self.search([
                ('nama_pemesanan', '=', record.nama_pemesanan),
                ('id', '!=', record.id)
            ])
            if existing_reservation:
                raise exceptions.ValidationError('Nama Pemesanan sudah ada.')

    @api.constrains('ruangan_id')
    def check_nama_ruangan(self):
        for record in self:
            existing_room = self.search([
                ('ruangan_id', '=', record.ruangan_id.id),
                ('id', '!=', record.id)
            ])
            if existing_room:
                raise exceptions.ValidationError('Nama Ruangan sudah ada.')