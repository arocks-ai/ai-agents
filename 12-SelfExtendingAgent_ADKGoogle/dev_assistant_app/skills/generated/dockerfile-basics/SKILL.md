
---
name: dockerfile-basics
description: >
  Technical reference for Dockerfiles, including their structure, common instructions, best practices, and examples. Use when the user asks about building Docker images, containerization, or optimizing Docker builds.
metadata:
  version: '1.0'
  author: dev-assistant
---

## 1. Executive Summary
A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image. Docker can read these instructions and build an automated image. Dockerfiles are essential for defining the environment and dependencies of an application, ensuring consistency across different environments, and enabling efficient, repeatable builds of Docker images. They provide a clear, declarative way to specify how a Docker image should be constructed, from the base operating system to the application code and its configurations.

## 2. Technical Concepts & Architecture
A Dockerfile consists of a series of instructions, each representing a command that is executed to build a layer in the Docker image. Each instruction creates a new read-only layer, and these layers are stacked on top of each other to form the final image. This layered architecture allows for efficient caching during builds and sharing of common layers between images.

Key concepts include:
*   **Base Image**: The `FROM` instruction specifies the parent image from which the new image will be built. Choosing a small, trusted base image (like Docker Official Images or Verified Publisher images) is crucial for security and performance.
*   **Instructions**: Each line in a Dockerfile is an instruction (e.g., `FROM`, `RUN`, `COPY`, `CMD`).
*   **Layers**: Each instruction in a Dockerfile creates a new layer in the image. When a Dockerfile is rebuilt, Docker reuses cached layers if the instruction and its context haven't changed, significantly speeding up the build process.
*   **Multi-stage Builds**: This technique allows you to create smaller, more secure images by using multiple `FROM` statements in a single Dockerfile. Intermediate build artifacts are discarded, ensuring the final image only contains the necessary runtime components.

## 3. Implementation & Quick Reference
Here's a quick reference for common Dockerfile instructions:

| Instruction | Description |
|-------------|-------------|
| `FROM <image>[:<tag>]` | Sets the Base Image for subsequent instructions. |
| `RUN <command>` | Executes any commands in a new layer on top of the current image and commits the results. |
| `CMD ["executable","param1","param2"]` | Provides defaults for an executing container. There can only be one `CMD` instruction in a Dockerfile. |
| `LABEL <key>=<value> [<key>=<value> ...]` | Adds metadata to an image. |
| `EXPOSE <port> [<port> ...]` | Informs Docker that the container listens on the specified network ports at runtime. |
| `ENV <key>=<value> ...` | Sets environment variables. |
| `ADD <src>... <dest>` | Copies new files, directories, or remote file URLs from `<src>` and adds them to the filesystem of the image at the path `<dest>`. |
| `COPY <src>... <dest>` | Copies new files or directories from `<src>` and adds them to the filesystem of the image at the path `<dest>`. Prefer `COPY` over `ADD` for local files. |
| `ENTRYPOINT ["executable", "param1", "param2"]` | Configures a container that will run as an executable. |
| `VOLUME ["/data"]` | Creates a mount point for external volumes. |
| `USER <user>[:<group>]` | Sets the user name (or UID) and optionally the user group (or GID) to use when running the image. |
| `WORKDIR /path/to/workdir` | Sets the working directory for any `RUN`, `CMD`, `ENTRYPOINT`, `COPY`, and `ADD` instructions that follow it. |
| `ARG <name>[=<default value>]` | Defines a build-time variable that users can pass to the builder with the `docker build --build-arg <varname>=<value>` command. |
| `ONBUILD <instruction>` | Adds a trigger instruction to an image that will be executed when the image is used as a base for another build. |
| `STOPSIGNAL <signal>` | Sets the system call signal that will be sent to the container to exit. |
| `HEALTHCHECK [OPTIONS] CMD command` | Tells Docker how to test a container to check if it is still working. |
| `SHELL ["executable", "parameters"]` | Allows the default shell used for the shell form of `RUN` commands to be overridden. |

## 4. Practical Examples

### Example 1: Simple Nginx Web Server

```dockerfile
# Use an official Nginx image as a base
FROM nginx:latest

# Copy a custom HTML file to the Nginx web root
COPY index.html /usr/share/nginx/html/index.html

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]
```

### Example 2: Python Flask Application

```dockerfile
# Use an official Python image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file first to leverage caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the Flask app will run on
EXPOSE 5000

# Define the command to run the Flask application
CMD ["python", "app.py"]
```

### Example 3: Multi-stage Build for a Go Application

```dockerfile
# Stage 1: Build the Go application
FROM golang:1.17-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o myapp .

# Stage 2: Create a minimal runtime image
FROM alpine:latest

WORKDIR /root/

# Copy the compiled binary from the builder stage
COPY --from=builder /app/myapp .

# Expose the port the application listens on
EXPOSE 8080

# Run the application
CMD ["./myapp"]
```

## 5. Performance & Best Practices

*   **Choose the Right Base Image**: Always start with a small, trusted base image (e.g., `alpine`, `slim` variants of official images). Smaller images reduce attack surface and download times. Docker Official Images and Verified Publisher images are recommended.
*   **Use Multi-stage Builds**: This is a powerful technique to create smaller final images by separating build-time dependencies from runtime dependencies.
*   **Optimize Caching**: Order your instructions from least to most frequently changing. Docker caches layers, and a change in an earlier layer invalidates all subsequent cached layers.
    *   Place `COPY` instructions for application code (which changes frequently) after installing dependencies (which change less frequently).
    *   Be more specific with `COPY` commands (e.g., `COPY requirements.txt .` instead of `COPY . .`) to limit cache busts.
*   **Minimize Layers**: While each instruction creates a layer, try to combine related `RUN` commands using `&&` to reduce the total number of layers.
*   **Avoid `latest` Tag**: Use specific tags for your base images (e.g., `python:3.9-slim-buster` instead of `python:latest`) to ensure repeatable builds and prevent unexpected breaking changes.
*   **Clean Up After `RUN` Commands**: Remove unnecessary files and caches created during `RUN` instructions to keep the image size down (e.g., `apt-get clean`, `rm -rf /var/lib/apt/lists/*`).
*   **Don't Run as Root**: Create a non-root user and switch to it using the `USER` instruction for security best practices.
*   **Use `.dockerignore`**: Exclude unnecessary files and directories (like `.git`, `node_modules`, `__pycache__`) from being copied into the image, which speeds up builds and reduces image size.

## 6. Diagnosis & Troubleshooting

*   **Build Failures**:
    *   **Read the Error Messages**: Docker build output provides detailed error messages. Pay close attention to the line number and the instruction that failed.
    *   **Inspect Intermediate Containers**: If a `RUN` command fails, you can often inspect the state of the intermediate container before the failure. Use `docker build --no-cache` to force a rebuild and see each step.
    *   **Debug with `docker run`**: Temporarily change your `CMD` or `ENTRYPOINT` to a shell (e.g., `CMD ["bash"]`) to interactively debug the container after a specific layer has been built.
*   **Image Size Issues**:
    *   **`docker history <image_id>`**: Use this command to see the layers of your image and their sizes, helping identify which instructions contribute most to the image size.
    *   **Multi-stage Builds**: Revisit your Dockerfile to implement multi-stage builds if you're not already using them.
    *   **Clean Up**: Ensure you're cleaning up temporary files and caches in your `RUN` commands.
    *   **Smaller Base Image**: Consider switching to an even smaller base image if possible.
*   **Application Not Running/Exiting**:
    *   **`CMD` vs. `ENTRYPOINT`**: Understand the difference. `CMD` provides default arguments to `ENTRYPOINT` or an executable. `ENTRYPOINT` configures a container that will run as an executable.
    *   **Correct Paths**: Verify that all file paths in `COPY`, `ADD`, `WORKDIR`, and `CMD` instructions are correct within the container's filesystem.
    *   **Permissions**: Ensure that the user running the application inside the container has the necessary permissions to access files and directories.
    *   **Logs**: Check the container logs using `docker logs <container_id>` for application-specific errors.
*   **Network Issues**:
    *   **`EXPOSE`**: Remember that `EXPOSE` only documents the port; it doesn't publish it. You need to use `-p` with `docker run` to map container ports to host ports.
    *   **Firewall**: Ensure no firewall rules are blocking traffic to the exposed ports.
