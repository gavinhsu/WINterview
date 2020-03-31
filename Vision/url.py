from django.urls import path
import Vision.views

path('vision/', Vision.HelloViews.View.as_view()),
