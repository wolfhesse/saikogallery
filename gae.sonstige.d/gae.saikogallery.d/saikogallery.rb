require 'rubygems'
require 'sinatra'

helpers do
  include Rack::Utils
  alias_method :h, :escape_html
end

class TvFolder
  attr_accessor :name
  attr_accessor :items
  def initialize 
    @items = []
  end
end

class TvItem
  attr_accessor :name
  attr_accessor :img_name
end

GALLERY_BASE_D = '/img.d/gallery'

post '/load_image' do
  @pimg = params[:pimg]
  @img_path = File.join(GALLERY_BASE_D, @pimg)
  erb :galcontent, :layout => false
end

get '/' do

  pr10 = TvItem.new
  pr10.name = 'pr 10'
  pr10.img_name = 'flyers/2000/pr10.jpg'

  pr11 = TvItem.new
  pr11.name = 'pr 11'
  pr11.img_name = 'flyers/2000/pr11.jpg'

  pr12 = TvItem.new
  pr12.name = 'pr 12'
  pr12.img_name = 'flyers/2000/pr12.jpg'

  pr13 = TvItem.new
  pr13.name = 'pr 13'
  pr13.img_name = 'flyers/2000/pr13.jpg'

  f2000 = TvFolder.new
  f2000.name = '2000'
  f2000.items << pr10
  f2000.items << pr11
  f2000.items << pr12
  f2000.items << pr13

  pr14 = TvItem.new
  pr14.name = 'pr 14'
  pr14.img_name = 'flyers/2001/pr14.jpg'

  sunproject = TvItem.new
  sunproject.name = 'sun project'
  sunproject.img_name = 'flyers/2001/sunproject.jpg'

  f2001 = TvFolder.new
  f2001.name = '2001'
  f2001.items << pr14
  f2001.items << sunproject

  pr18 = TvItem.new
  pr18.name = 'pr 18'
  pr18.img_name = 'flyers/2002/pr18.jpg'

  pr24 = TvItem.new
  pr24.name = 'pr 24'
  pr24.img_name = 'flyers/2002/pr24.jpg'

  talamasca = TvItem.new
  talamasca.name = 'talamasca'
  talamasca.img_name = 'flyers/2002/talamasca.jpg'

  f2002 = TvFolder.new
  f2002.name = '2002'

  f2002.items << pr18
  f2002.items << pr24
  f2002.items << talamasca

  pr25 = TvItem.new
  pr25.name = 'pr 25'
  pr25.img_name = 'flyers/2003/pr25.jpg'

  pr26 = TvItem.new
  pr26.name = 'pr 26'
  pr26.img_name = 'flyers/2003/pr26.jpg'

  pr27 = TvItem.new
  pr27.name = 'pr 27'
  pr27.img_name = 'flyers/2003/pr27.jpg'

  pr30 = TvItem.new
  pr30.name = 'pr 30'
  pr30.img_name = 'flyers/2003/pr30.jpg'

  pr31v1 = TvItem.new
  pr31v1.name = 'pr 31v1'
  pr31v1.img_name = 'flyers/2003/pr31v1.jpg'

  f2003 = TvFolder.new
  f2003.name = '2003'

  f2003.items << pr25
  f2003.items << pr26
  f2003.items << pr27
  f2003.items << pr30
  f2003.items << pr31v1

  anjuna = TvItem.new
  anjuna.name = 'anjuna'
  anjuna.img_name = 'flyers/2005/anjuna.jpg'

  finalfront = TvItem.new
  finalfront.name = 'final cut'
  finalfront.img_name = 'flyers/2005/finalfront.jpg'

  sbk = TvItem.new
  sbk.name = 'sbk'
  sbk.img_name = 'flyers/2005/sbk.jpg'

  f2005 = TvFolder.new
  f2005.name = '2005'

  f2005.items << anjuna
  f2005.items << finalfront
  f2005.items << sbk

  star = TvItem.new
  star.name = '10-star'
  star.img_name = 'pix/10star.jpg'

  greenkiss = TvItem.new
  greenkiss.name = 'green kiss'
  greenkiss.img_name = 'pix/greenkiss.jpg'

  icon = TvItem.new
  icon.name = 'icon'
  icon.img_name = 'pix/icon.png'

  ### %w(pr10 pr11 pr12).each do |p|
  ### i=TvItem.new
  ### i.name = "Bild #{p}"
  ### i.img_name = "2000/#{p}.jpg"
  ### f2001.items << i
  ### end

  # aufbau folders

  fviz0 = TvFolder.new
  fviz0.name = 'flyer'

  fviz0.items << f2000
  fviz0.items << f2001
  fviz0.items << f2002
  fviz0.items << f2003
  fviz0.items << f2005


  fviz1 = TvFolder.new
  fviz1.name = 'random'

  fviz1.items << star
  fviz1.items << greenkiss
  fviz1.items << icon


  fviz2 = TvFolder.new
  fviz2.name = 'illustrations'



  @tl = TvFolder.new
  @tl.name = 'visual'
  @tl.items << fviz0
  @tl.items << fviz1
  @tl.items << fviz2

  erb :index, :layout => false
end


post '/' do
  redirect '/'
end
