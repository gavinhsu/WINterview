from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class visionView(templates):
    template_name = 'vision.html'
    import io
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\asus\Desktop\MIS Project\mis project-e675889a0b43.json"
    # Imports the Google Cloud client library
    from google.cloud import vision
    from google.cloud.vision import types

    def detect_faces(path):
        """Detects faces in an image."""
        from google.cloud import vision
        import io
        import os
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=r"C:\Users\asus\Desktop\MIS Project\mis project-e675889a0b43.json"
        client = vision.ImageAnnotatorClient()

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = client.face_detection(image=image)
        faces = response.face_annotations

        # Names of likelihood from google.cloud.vision.enums
        likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                           'LIKELY', 'VERY_LIKELY')
        print('Faces:')


        # printing the possibilities of each emotion in for loop
        for face in faces:
            print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
            print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
            print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                        for vertex in face.bounding_poly.vertices])

            # vertices: 臉的各個頂點
            print('face bounds: {}'.format(','.join(vertices)))

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        # working the function detect_faces(path of pic)
        detect_faces(r'C:\Users\asus\Desktop\hsusmile.jpg')
