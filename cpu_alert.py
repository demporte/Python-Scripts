import os 
import psutil
import socket
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import logging
from logging.handlers import SMTPHandler


#get host information
hostname = socket.gethostname()
print(hostname)

# #get necessary information for report
#cpu_utilization = psutil.cpu_percent(interval=1)
cpu_utilization = 90
disk_utilization = psutil.disk_usage('/')
network_traffic = psutil.net_io_counters()


#function to send the email
def send_email(recipient, body, subject): 
    #set up Secure SMTP server 
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("EMAIL_PASSWORD")

    #create email 
    email = MIMEMultipart()
    email["FROM"] = sender_email
    email["To"] = recipient
    email["Subject"] = subject
    email.attach(MIMEText(body, "html"))

    try:
        # Connect to the SMTP server securely
        with smtplib.SMTP(smtp_server, smtp_port) as email_server:
            email_server.starttls()  # Initiate secure TLS connection
            email_server.login(sender_email, sender_password)
            email_server.sendmail(sender_email, recipient, email.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")




#set up logging file 
logging.basicConfig(filename="test_log.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

#format bytes for human readability
#bulls kill mega gigantic Tyrannosaurus
def format_output(byte_amount):
    units = ["B","KB","MB","GB","TB"]
    byte_count = byte_amount
    index = 0 

    while byte_count > 1024 and index < len(units) - 1 :
        byte_count /= 1024.9
        index += 1 #determine which unit to use 
         
    return f"{byte_count:.2f} {units[index]}"


def create_body(threashold,cpu, action_required, diskT, diskU, diskF, diskP,netS,netR):
   # email_body = "CPU Utilization has exceeded the " + str(threashold)+  "% threshold " + str(action_required)
    email_body = f"""
<html>
  <body>
    <h1>Security Alert: {action_required}</h1>
    <p>CPU utilization has exceeded the threshold of <strong>{threashold}</strong>.</p>
   

     <h2>Aditional Details</h2>
     <p>CPU utilization: {cpu}%</p>
     <p>Disk Bytes Total : {diskT}</p>
     <p>Disk Bytes Used: {diskU}</p>
     <p>Disk Bytes Free: {diskF}</p>
     <p>Disk Percentage: {diskP}%</p>
     <p>Network Bytes Sent: {netS}</p>
     <Network Bytes Resieved: {netR}</p>

 

  </body>
</html>
"""
    return email_body
   



def main():
#obtain new values 
    disk_total = format_output(disk_utilization.total)
    disk_used = format_output(disk_utilization.used)
    disk_free = format_output(disk_utilization.free)
    disk_percent = disk_utilization.percent
    net_sent = format_output(network_traffic.bytes_sent)
    net_recv = format_output(network_traffic.bytes_recv)

#log these values
    logging.info("CPU Utilization: " + str(cpu_utilization) + "%")
    logging.info("Disk - total usage: " + str(disk_total))
    logging.info("Disk - total used: " + str(disk_used))
    logging.info("Disk - total free:" + str(disk_free))
    logging.info("Disk - percentage:" + str(disk_percent)+ "%")
    logging.info("Network traffic Bytes sent: " + str(net_sent))
    logging.info("Network traffic Bytes recv" + str(net_recv))

#CPU thresholds login

    if cpu_utilization >= 90:
        subject = "CRITICAL CPU Utilization for: " + str(hostname) 
        action = "IMMEDIATE ACTION IS REQUIRED"
        body = create_body(90, cpu_utilization,action,disk_total,disk_used,disk_free,disk_percent, net_sent,net_recv)
        #body = "CPU utilization has exceeded the threshold."
        recipient = "desbballqeen@gmail.com"
        send_email(recipient, body, subject)
    elif cpu_utilization >= 70:
        subject = "WARNING CPU Utilization for: " + str(hostname)
        action = "INVESTIGATION IS REQUIRED"
        body = create_body(70, cpu_utilization,action,disk_total,disk_used,disk_free,disk_percent, net_sent,net_recv)
        #body = "CPU utilization has exceeded the threshold."
        recipient = "desbballqeen@gmail.com"
        send_email(recipient, body, subject)


if __name__ == "__main__":
    main()
