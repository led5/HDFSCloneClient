from client import Client
import os

def main():

    # Create Clients:
    c1 = Client('http://35.162.89.185:5000', 'AKIAWADW7U477OITTK6J', 'd9HDxd5pXR5UnQ4JZKoyX2Oo4WyPrDfC5bdWVaKc',
                'whatever214', '200MB.zip', data_filename_local='200MB.zip')

    c2 = Client('http://35.162.89.185:5000', 'AKIAWADW7U477OITTK6J', 'd9HDxd5pXR5UnQ4JZKoyX2Oo4WyPrDfC5bdWVaKc',
                'whatever214', '1GB.zip', data_filename_local='1GB.zip')

    c3 = Client('http://35.162.89.185:5000', 'AKIAWADW7U477OITTK6J', 'd9HDxd5pXR5UnQ4JZKoyX2Oo4WyPrDfC5bdWVaKc',
                'whatever214', 'eternity.jpg', data_filename_local='eternity.jpg')

    # Read from s3 bucket:
    # c1.get_data()
    # c2.get_data()
    # c3.get_data()

    # Create and Write:

    # size1 = os.stat('200MB.zip').st_size
    # c1.create_write('200MB.zip', 'medium.zip', size_in_bytes=size1)

    # size2 = os.stat('1GB.zip').st_size
    # c2.create_write('1GB.zip', 'very_large.zip', size_in_bytes=size2)

    # size3 = os.stat('eternity.jpg').st_size
    # c3.create_write('eternity.jpg', 'small.jpg', size_in_bytes=size3)

    # Read:
    #c1.read('medium.zip', 'medium_returned.zip')
    # c2.read('very_large.zip', 'very_large_returned.zip')
    c3.read('small.jpg', 'small_returned.jpg')

    # List:
    #c1.list('medium.zip')
    # c2.list('very_large.zip')
    # c3.list('small.jpg')


if __name__ == '__main__':
    main()
