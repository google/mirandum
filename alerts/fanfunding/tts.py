import tempfile
import subprocess, os
import urllib

SOUND_PATH = "/webapps/alerts/static/sounds"

def get_sound(url):
    """Write a given URL to disk, maintaining extension."""
    u = urllib.urlopen(url)
    ext = url.split(".")[-1]
    if len(ext) != 3:
        ext = "wav"
    tf = tempfile.NamedTemporaryFile(suffix=".%s" % ext, delete=False)
    tf.write(u.read())
    tf.close()
    return tf.name

def generate_text(text):
    """Generate the svox output for the given text"""
    tf = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tf.close()
    args = ['pico2wave']
    args.extend(['-l','en-US'])
    args.extend(['-w', tf.name, '{0}'.format(text.encode('utf-8'))])
    subprocess.check_output(args)
    return tf.name

def combine_files(sound_name, text_name, id):
    """Combine the two files."""
    # Convert both files to 44.1Khz with 2 channels
    for i in [sound_name, text_name]:
        args = "sox %s -r 44100 -c 2 %s-out.wav rate" % (i, i)
        subprocess.check_output(args.split(" "))
    args = ['sox', '%s-out.wav' % sound_name, '-c', '2', '%s-out.wav' % text_name, '-r', '44100', os.path.join(SOUND_PATH, '%s.wav' % id)]
    subprocess.check_output(args)
    return True

def do_it(url, text, id):
    sound_name = get_sound(url)
    text_name = generate_text(text)
    combine_files(sound_name, text_name, id)


