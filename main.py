from ms_graph_auth import * 
from form_filler import * 
import time

graph_auth = MsGraphAuth('parameters.json')
def fill_form():
    global graph_auth
    # Logging in
    if graph_auth.log_in(): 
        # Getting data from the api 
        data = graph_auth.get_data()
        # Looking at the most recent message
        latest_message = data['value'][0]
        # Body preview, the attendance form that my teacher uploads just contains the link, so the link is there in preview as well
        prev = latest_message['bodyPreview']
        prev_arr = prev.split(' ')
        if '<YOUR_TEACHER\'S_USERNAME>' in prev_arr: # Making sure that it is uploaded by the correct teacher
            print('One new message from <your teacher>, checking if the message has forms link')
        else:
            print('No new messages found.')
            return False # Return statement to ensure that the function does not proceed further

        url = None

        # Looking for the url by iterating through all the elements of body preview, I could not figure out the regex for this.
        for element in prev_arr:
            if 'href' in element:
                url = element[6:-1]
                print('Form link found')
                print('URL = ', url)
                break 

        form_filler = FormsFiller(url, 'Present')
        form_filler.log_in()
        form_filler.fill_form()
        return True 

while True: 
    current_time = time.strftime('%H:%M')
    if current_time > '13:15' and current_time < '13:45': # My teacher uploads at this time
        if fill_form():
            print()
            break 
        else: 
            print()
            time.sleep(10) # Avoiding spamming the api
