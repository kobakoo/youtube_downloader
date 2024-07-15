from __future__ import unicode_literals

from fastapi import FastAPI
from reactpy import component, html,hooks
from reactpy.backend.fastapi import configure
import yt_dlp



def download_video(url,set_video_url):
  ydl_opts = {}
  with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info: object = ydl.extract_info(url, download=False)
    # print(info)
    set_video_url(info["url"])

@component
def DownloadButton(url,set_video_url):
  def handle_event(event):
    print(url);
    download_video(url,set_video_url)

  return html._(
    html.div({"class":"max-w-md mx-auto mt-5"},
             html.button({"on_click": handle_event,
                          "class": "text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 me-2 mb-2"},
                         "ダウンロード")
    )
  )

@component
def Search(url,set_value):
  def handle_change(event):
    set_value(event["target"]["value"])
    # print(event["target"]["value"])

  return html._(
    html.label({"class_name":"block mb-2 text-sm font-medium text-gray-90 max-w-md mx-auto"},
      "Youtube Video Url ",
    ),
    html.span(
      html.input(
        {"value": url, "on_change": handle_change,"class_name":"bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 max-w-md mx-auto"}),
    )
  )


@component
def Body():
    value, set_value = hooks.use_state("")
    video_url, set_video_url = hooks.use_state("")

    return html._(
                  html.h1({"class_name":"mb-4 text-4xl font-extrabold leading-none tracking-tight text-gray-900 md:text-5xl lg:text-6xl items-center justify-center w-full text-center mt-8"},"Youtube Downloader"),
                  html.script({"src": "https://cdn.tailwindcss.com"}, ""),
                  Search("test",set_value),
                  DownloadButton(value,set_video_url),
                  html.video({"controls":True,"class":"rounded-lg mx-auto w-md"},
                             (html.source({"src":video_url,"type":"video/mp4"}),"Your browser does not support the video tag.")
                             ),
                  f"original video url is here! ⇨ {video_url}"
                )


app = FastAPI()
configure(app, Body)
