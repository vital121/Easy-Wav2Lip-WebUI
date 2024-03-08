from flask import Flask, request, redirect, url_for, render_template, send_file
import configparser
import os
import subprocess

app = Flask(__name__)

# Создаем папки 'uploads' и 'outputs', если они не существуют
os.makedirs('uploads', exist_ok=True)
os.makedirs('outputs', exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        video = request.files['video']
        audio = request.files['audio']
        quality = request.form.get('quality')

        # Сохраняем видео и аудио файлы в папку 'uploads'
        video_path = os.path.join('uploads', video.filename)
        audio_path = os.path.join('uploads', audio.filename)
        video.save(video_path)
        audio.save(audio_path)

        config = configparser.ConfigParser()
        config.read('config.ini')
        config.set('OPTIONS', 'video_file', video_path)
        config.set('OPTIONS', 'vocal_file', audio_path)
        config.set('OPTIONS', 'quality', quality)

        with open('config.ini', 'w') as configfile:
            config.write(configfile)

        subprocess.run(["python", "run.py"])

        # Перемещаем обработанный видео файл в папку 'outputs'
        output_file = os.path.join('outputs', video.filename)
        os.replace(video_path, output_file)

        return render_template('result.html', output_file=output_file)

    return render_template('index.html')

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    output_file = os.path.join('outputs', filename)
    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
