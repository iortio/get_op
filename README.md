# Install Python example repo from server (iort_example_python_sum)
 curl -s https://raw.githubusercontent.com/iortio/get_op/main/get_op.py | sudo python3 - -r https://github.com/iortio/iort_example_python_sum.git -t PAT_TOKEN

# Install Makefile (C) example repo from server (iort_example_c_script)
 curl -s https://raw.githubusercontent.com/iortio/get_op/main/get_op.py | sudo python3 - -r https://github.com/iortio/iort_example_c_script.git -t PAT_TOKEN

# Install and run FastAPI Docker example repo from server (iort_example_docker)
 curl -s https://raw.githubusercontent.com/iortio/get_op/main/get_op.py | sudo python3 - -r https://github.com/iortio/iort_example_docker.git -t PAT_TOKEN

# Build environment
 curl -s https://raw.githubusercontent.com/iortio/get_op/main/build_environment.py | sudo python3 - -r https://github.com/iortio/environment_dotest.git -t PAT_TOKEN

# Use of repo from Python Script

 from iort_example_python_sum.main import main as sum314

 sum314(3,4)
