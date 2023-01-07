FROM python:3.10

RUN apt-get update && apt-get install -y ffmpeg

RUN pip install -U pip
RUN pip install spleeter
# other packages
RUN pip install matplotlib librosa "fastapi[all]" yt-dlp
WORKDIR /backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]

# docker run -d --name spleeter_test -v /mnt/c/Users/amach/OneDrive/デスクトップ/HelpYourCopy/backend/:/backend/ -p 8080:8080 b0f29fc85e4f