import boto3
import os
from math import ceil
import requests


class Client:
    def __init__(self, name_node_url, aws_access_key, aws_secret_key, s3_bucket_name, data_filename_s3,
                 data_filename_local='data.txt', s3_region_name='us-west-2'):
        assert type(name_node_url) is str
        assert type(aws_access_key) is str
        assert type(aws_secret_key) is str
        assert type(s3_bucket_name) is str
        assert type(data_filename_s3) is str
        assert type(data_filename_local) is str
        assert type(s3_region_name) is str
        self.name_node_url = name_node_url
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.s3_bucket_name = s3_bucket_name
        self.data_filename_s3 = data_filename_s3
        self.data_filename_local = data_filename_local
        self.s3_region_name = s3_region_name
        self.s3_data_size = None
        self.s3_data_blocks = None

    def get_data(self):
        """To download input file from S3 bucket."""

        # Establish connection with S3 bucket:
        s3 = boto3.client('s3', region_name=self.s3_region_name, aws_access_key_id=self.aws_access_key,
                          aws_secret_access_key=self.aws_secret_key)

        # Save data_filename_s3 to data_filename_local:
        s3.download_file(self.s3_bucket_name, self.data_filename_s3, self.data_filename_local)
        self.s3_data_size = os.stat(self.data_filename_local).st_size

    @staticmethod
    def break_into_blocks(filename, LoB, block_size=2**27):
        """
            Split operation.

            Parameters:
            filename (str): File that will be split and stored.
            LoB (dict): List of blocks from NameNode.
            block_size: Block size in bytes.

            Returns:
            blocks (dict): chunks of block data

        """

        blocks = {}
        file_size_bytes = os.stat(filename).st_size
        number_of_blocks = len(LoB)
        with open(filename, 'rb') as f:
            for block_filename in LoB:
                with open(block_filename, 'wb') as b:
                    b.write(f.read(block_size))
                    blocks[block_filename] = block_filename
        return blocks

    @staticmethod
    def write_block_to_data_nodes(block_filename, data_nodes):

        responses = []
        with open(block_filename, 'rb') as block:
            block_data = block.read()
        payload = {block_filename: block_data}
        print(payload)

        for url in data_nodes:
            node_url = Client.fix_extension(url, '/write')
            print(type(node_url), node_url)
            print(payload)
            r = requests.post(url=node_url, files=payload)
            responses += [r]

        all_uploads_failed = True
        for response in responses:
            if response.status_code == 200:
                all_uploads_failed = False
        if all_uploads_failed:
            raise Exception("all uploads for {0} failed".format(block_filename))
        return responses

    @staticmethod
    def fix_extension(url, extension):
        if url[-1] == '/':
            extension = extension[1:]
        return url + extension

    def create_write(self, local_filename, sufs_filename, size_in_bytes, block_size=2**27):
        """
            Create and write new file into SUFS.

            Parameters:
            local_filename (str): File that will be split and stored.
            sufs_filename (str): Where data is stored.
            size_in_bytes (int): Size of local_filename
            block_size (int): block size in bytes

            Returns:
            responses

        """
        # Request LoB from NameNode:
        params = {sufs_filename: size_in_bytes} # {nameofnewfile: size_in_bytes}
        url = self.name_node_url + '/create'
        response = requests.get(url, params)

        # Check NameNode response:
        if response.status_code != 200:
            raise Exception("requests.get failed: status code {0}".format(response.status_code))
        LoB = response.json()
        print(LoB)

        # Split files in LoB:
        blocks = self.break_into_blocks(local_filename, LoB, block_size)
        print(blocks)

        # Write chunks to data nodes:
        responses = []
        for _, block_filename in blocks.items():
            responses.append(self.write_block_to_data_nodes(
                block_filename, LoB[block_filename]))
        return responses

    @staticmethod
    def sort_keys(keys):
        sequence = {}
        for key in keys:
            sequence_number = int(key.split('_')[-1])
            sequence[sequence_number] = key
        sorted_keys = []
        for key in sorted(sequence.keys()):
            sorted_keys.append(sequence[key])
        return sorted_keys

    @staticmethod
    def merge_blocks_into_file(blocks, filename):
        """Merge data from data nodes and save into local file."""

        key_order = Client.sort_keys(blocks.keys())
        data_list = []
        for key in key_order:
            data_list.append(blocks[key])
        # Open filename:
        with open(filename, 'wb') as f:
            # Write data into local file:
            for block_data in data_list:
                for line in block_data:
                    f.write(line)
        #print(key_order)

    def read(self, sufs_filename, local_filename):
        """
            Read file from SUFS and save to client's local disk.
            
            Parameters:
            sufs_filename (str): File from SUFS
            local_filename (str): Where data will be stored locally

            Returns: 
            none
            
        """

        # Request file from SUFS:
        params = {sufs_filename: sufs_filename}
        url = self.fix_extension(self.name_node_url, '/read')
        response = requests.get(url, params)

        # Check NameNode response:
        if response.status_code != 200:
            raise Exception('Name node response to read: {0}'.format(response.status_code))
        resp = response.json() # {block_id: [url1, url2, url3....]}

        # Read block from data nodes:
        blocks = {} # {block_id: data}
        for block in resp:
            successfully_retrieved_block = False
            for url in resp[block]:
                url = self.fix_extension(url, '/read')
                params = {'filename': block}
                response = requests.get(url, params)
                if response.status_code == 200:
                    successfully_retrieved_block = True
                    blocks[block] = response
                    break
            if not successfully_retrieved_block:
                raise Exception('block {0} failed to download from all nodes'.format(block))
        self.merge_blocks_into_file(blocks, local_filename)

    def list(self, filename):
        """Display file."""

        # Request LoB for filename from NameNode:
        url = self.fix_extension(self.name_node_url, '/list')
        parameters = {filename: filename}
        response = requests.get(url=url, params=parameters)

        # Check NameNode Response:
        if response.status_code != 200:
            raise Exception('name node returned status code {0}'.format(response.status_code))
        data = response.json()
        print(data)

        return data
