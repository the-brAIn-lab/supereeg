import re
from main_config import main_config


# Function to replace specific SBATCH directives
def update_sbatch_directive(content, directive, new_value):
    """Replace or add an SBATCH directive while preserving everything else"""
    # Pattern to match #SBATCH --directive=value or #SBATCH --directive value
    pattern = rf'(#SBATCH\s+--{directive}\s*[= ]\s*)[^\n]+'
    
    # If the directive exists, replace it
    if re.search(pattern, content):
        content = re.sub(pattern, rf'\1{new_value}', content)
    else:
        # If it doesn't exist, add it at the beginning after #!/bin/bash
        shebang_match = re.search(r'^(#!/bin/bash\n)', content)
        if shebang_match:
            insert_pos = shebang_match.end()
            content = content[:insert_pos] + f'#SBATCH --{directive}={new_value}\n' + content[insert_pos:]
        else:
            # If no shebang, add at the top
            content = f'#SBATCH --{directive}={new_value}\n' + content
    
    return content

pipeline = ["file_io","pyFR_locs","full_mats","ave_mats","recon"]
for i in range(len(pipeline)):
    # Read the existing SH file
    path_sh = main_config["scripts"]+"/"+pipeline[i]+"/run_job.sh"
    path_output = main_config["scripts"]+"/"+pipeline[i]+f"/{pipeline[i]}_log.txt"
    path_error = main_config["scripts"]+"/"+pipeline[i]+f"/{pipeline[i]}_error.txt"
    with open(path_sh, 'r') as f:
        content = f.read()

    # Only update the specific settings we care about
    content = update_sbatch_directive(content, 'output', path_output)
    content = update_sbatch_directive(content, 'error', path_error)
    content = update_sbatch_directive(content, 'mail-user', main_config['email'])


    # Write the updated content back
    with open(path_sh, 'w') as f:
        f.write(content)


# Read the existing SH file for pipeline sh
path_sh = main_config["scripts"]+"/run_pipeline.sh"
path_output = main_config["scripts"]+"/pipeline_log.txt"
path_error = main_config["scripts"]+"/pipeline_error.txt"
with open(path_sh, 'r') as f:
    content = f.read()

 # Only update the specific settings we care about
content = update_sbatch_directive(content, 'output', path_output)
content = update_sbatch_directive(content, 'error', path_error)
content = update_sbatch_directive(content, 'mail-user', main_config['email'])


# Write the updated content back
with open(path_sh, 'w') as f:
    f.write(content)
