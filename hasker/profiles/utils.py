from uuid import uuid4


def get_image_path(instance, file_name):
    return 'avatars/' + str(uuid4()) + '.' + file_name.split('.')[-1]