require 'appengine-rack'
AppEngine::Rack.configure_app(
  :application => 'saikogallery',
  :version => 1)
require 'saikogallery'
run Sinatra::Application
