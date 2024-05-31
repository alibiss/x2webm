import os, sys, argparse, json, subprocess as sb
from pathlib import Path as path

parser = argparse.ArgumentParser(
    prog = "x2webm",
    description = "Encode videos in a tweet to webm without downloading them."
)

parser.add_argument("URL")
parser.add_argument("-b:v", "--vb", dest="bitrate", required=False, default="1M")
try:
    args = parser.parse_args()
except:
    input("Press Enter to exit..")

outdir = os.path.join(path.home(), "Downloads")
outdir = outdir if os.path.isdir(outdir) else path.home()

def encode(url, filename):
    OPTIONS = "-c:v libvpx-vp9 -b:v %s -an" % args.bitrate
    OUTPUT = os.path.join(outdir, "%s.webm" % filename)

    try:
        sb.run("ffmpeg -v quiet -stats -i \"%s\" %s \"%s\"" % (url, OPTIONS, OUTPUT))
    except FileNotFoundError:
        print("ffmpeg was not found..")
        input("Press Enter to exit..")
        sys.exit(1)
    
def getBest(formats):
    matches = list(filter(lambda o: o["protocol"] == "https", formats))
    return matches[-1]["url"]

def parseRes(responses):
    for i, res in enumerate(responses):
        if len(responses) > 1:
            print("Encoding video %s/%s" % (i+1, len(responses)))

        obj = json.loads(res)
        filename = obj["id"]

        if (len(responses) > 1):
            filename += "-" + str((i+1))

        encode(getBest(obj["formats"]), filename)

try:
    responses = sb.check_output(["yt-dlp", "-j", args.URL]).splitlines()
except FileNotFoundError:
    print("yt-dlp was not found..")
    input("Press Enter to exit..")
    sys.exit(1)
except:
    sys.exit(1)

parseRes(responses)