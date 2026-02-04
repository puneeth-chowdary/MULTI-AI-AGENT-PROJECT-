FROM jenkins/jenkins:lts

USER root

# Install Docker CLI + basic tools (Debian-native, stable)
RUN apt-get update && \
    apt-get install -y \
        docker.io \
        git \
        curl \
        python3 \
        python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Allow Jenkins user to run Docker
RUN usermod -aG docker jenkins

USER jenkins
