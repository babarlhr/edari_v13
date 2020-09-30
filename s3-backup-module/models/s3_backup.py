
from odoo import models, fields,service, api, _
from odoo.exceptions import Warning
import os.path
import sys,glob, os, boto
import boto3
from botocore.exceptions import ClientError
from boto.s3.key import Key
import logging
from datetime import timedelta,datetime,date
import jsonrpc


class Configuration(models.Model):


	_name = 's3.configure'

	name = fields.Char(String='Name', required=True, store=True)
	auth_key = fields.Char(String='User Authentication Key', required=True)
	auth_secret = fields.Char(
		String='User Authentication Secret', required=True)
	bucket_name = fields.Char(String='S3 Bucket Name', required=True)
	source = fields.Char(String="Source Location", default="/odoo/backups",
						 help="this will be the location where the auto backup has saved the file in your local drive")
	destination = fields.Char(String="Destination Location",
							  default="/", help="this will the s3 bucket source location")


	@api.model
	def submit_values(self):
		recs = self.env['s3.configure'].search([])
		for x in recs:
			response=x.upload_files(x.source)
			print (response)
			if response == True:
				self.create_entity_status()


	def create_entity_status(self):
		pass
		# try:

		# 	comp_rec = self.env['res.company'].search([])
		# 	srv, db = comp_rec[0].db_url_ecube, comp_rec[0].db_database
		# 	user , pwd = comp_rec[0].db_user_ecube, comp_rec[0].db_password_ecube
		# 	common =  jsonrpc.ServerProxy('%s/xmlrpc/2/common' % srv)
		# 	common.version()
		# 	uid = common.authenticate(db, user, pwd, {})
		# 	api = jsonrpc.ServerProxy('%s/xmlrpc/2/object' % srv)

		# 	entity = self.env['psc.entity'].search([],limit=1)
		# 	date_time = datetime.today()
		# 	get_date = str(date_time).split(' ')
		# 	date = get_date[0]
		# 	backup_status = []
		# 	date_time = str(date_time)
		# 	backup_status.append({
		# 			'date': get_date[0],
		# 			'date_time': date_time,
		# 			'psc_entity': entity.master_id,
		# 			})

		# 	if len(backup_status) > 0:

		# 		master = 8
		# 		temp = api.execute_kw(db, uid, pwd, 'backup.status', 'entity_backup_status_crearte', [int(master)],{
		# 			'backup_status':backup_status,
		# 			})
		# except Exception as e:
		# 	print ("Connection Error...{}".format(e))
		# 	return False
	


	def upload_files(self,path):

		session = boto3.Session(
			aws_access_key_id=self.auth_key,
			aws_secret_access_key=self.auth_secret,
			region_name='eu-west-1'
		)

		
		s3 = session.resource('s3')
		s3_client = session.client('s3')
		bucket = s3.Bucket(self.bucket_name)
	 
		# list_of_files = glob.glob(path+'/*') # * means all if need specific format then *.csv
		# latest_file = max(list_of_files, key=os.path.getctime)

		# with open(latest_file, 'rb') as data:
		filename, content = self.get_backup()
		path = os.path.join(filename)
		try:
			# result = bucket.put_object(Key=latest_file[len(path):], Body=data)
			result = bucket.put_object(Key=path, Body=content)
		except Exception as e:
			logging.error(e)
			return False
		return True
			
	

	# def get_path_and_content(self):
	# 	"""
	# 	Get the Path with Filename and the DB-backup-content
	# 	:return: tuple(path: string, content: binary)
	# 	"""
	# 	filename, content = self.get_backup()
	# 	path = os.path.join(self.upload_path, filename)
	# 	return path, content

	def get_backup(self, dbname=None, backup_format='zip'):
		"""
		Get backup with content
		:param dbname: string
		:param backup_format: string
		:return: tuple(filename: string, dump_data: binary)
		"""
		if dbname is None:
			dbname = self._cr.dbname
		ts = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
		filename = "%s_%s.%s" % (dbname, ts, backup_format)
		dump_stream = service.db.sudo().dump_db(dbname, None, backup_format)
		return filename, dump_stream
# sudo pip install boto  boto3 urllib3==1.22 botocore jsonrpclib
