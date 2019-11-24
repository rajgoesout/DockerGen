FROM golang
COPY . /go/src/github.com/{{ composeProjectName }}/
RUN go install github.com/{{ composeProjectName }}
ENTRYPOINT /go/bin/{{ composeProjectName }}
