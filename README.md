# Install repo from server. iort_example_python_sum
curl -s https://raw.githubusercontent.com/iortio/get_op/main/get_op.py | python3 - -r iortio/iort_example_python_sum.git -t PAT_TOKEN -p /usr/local/lib/python3.8/dist-packages

# Use of repo from Python Script

 from iort_example_python_sum.main import main as sum314

 sum314(3,4)
