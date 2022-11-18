import streamlit as st
from PIL import Image
import pandas as pd
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ALL DATASET 
bowling_data = pd.read_csv('bowling.csv')
batting_data = pd.read_csv('batting.csv')
PT = pd.read_csv('IPLPointsTable.csv')

# SIDE BAR WITH IMAGE LOGO
st.sidebar.image("IPL.jpg", use_column_width=True)

# SIDE BAR OR NAVIGATION
with st.sidebar:
    selected = option_menu('IPL 2022',
                            ['IPL Teams Info','Batsman Performance', 'Bowler Performance'])


# ANOTHER PAGE START PAGE 1
#==================================================================#
#==================================================================#
#==================================================================#

def TeamsInfo():
    #st.title('IPL 2022 Teams Information')
    
    # load dataset
    match_data = pd.read_csv('IPL_Matches_2022.csv')
    teams = match_data['Team1'].drop_duplicates()
    teams_df = pd.DataFrame(teams)
    teams_df = teams_df.reset_index()
    teams_df.drop(columns=['index'], inplace=True)
    st.title('Teams Name Who Played IPL 2022')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('#### 1. Mumbai Indians')
    with col2:
        st.write('#### 2. Chennai Super Kings')
    with col3:
        st.write('#### 3. Royal Challengers Bangalore')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('#### 4. Rajasthan Royals')
    with col2:
        st.write('#### 5. Sunrisers Hyderabad')
    with col3:
        st.write('#### 6. Punjab Kings')

    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('#### 7. Kolkata Knight Riders')
    with col2:
        st.write('#### 8. Lucknow Super Giants')
    with col3:
        st.write('#### 9. Delhi Capitals')

    col1, col2 = st.columns(2)
    with col1:
        st.write('#### 10. Gujarat Titans')

    st.write('---------------------------------------')

    # Qualified Teams
    #st.write('## 🙶 Qualified Teams 🙷')
    st.title('Qualified Teams')

    col1, col2 = st.columns(2)
    with col1:
        st.write('#### 1. Gujarat Titans')
    with col2:
        st.write('#### 2. Rajasthan Royals')

    col1, col2 = st.columns(2)
    with col1:
        st.write('#### 3. Royal Challengers Bangalore')
    with col2:
        st.write('#### 4. Lucknow Super Giants')
    
    st.write('-------')

    # Teams who played Final IPL 2022
    #st.write('## 🙶 Teams Who Played Finale in IPL 2022 🙷')
    st.title('Teams Who Played Finale')

    col1, col2 = st.columns(2)
    with col1:
        st.write('#### 🏅 1. Gujarat Titans')
    with col2:
        st.write('#### 🏅 2. Rajasthan Royals')

    st.write('-------')

    # Winning team
    #st.write('## 🙶🏆 IPL 2022 Winning Team 🏆🙷')
    st.title('🏆 IPL 2022 Winning Team 🏆')

    st.write('#### 🏆 1. Gujarat Titans')

    st.write('-------')
    
    # Points table
    PT.drop(columns=['Unnamed: 0'], inplace=True)
    #st.write('## 🙶 IPL 2022 Points Table 🙷')
    st.title('IPL 2022 Points Table')
    st.table(PT)
    
    st.write('-------')


    # Number of matches won by each team
    def MatchWonByTeam(Team_Name):
        result = match_data[match_data['WinningTeam'] == Team_Name].shape[0]
        return result

    n = []
    for i in teams_df['Team1']:
        n.append(MatchWonByTeam(i))
            
    teams_df['Number of matches won by each team in IPL 2022'] = n
    teams_Name = teams_df.rename(columns={'Team1':'Teams Name in IPL 2022'})
    cols = teams_Name['Teams Name in IPL 2022']
    values = teams_Name['Number of matches won by each team in IPL 2022']

    # pie plot
    #st.write('## 🙶 Number of Matches Won by Each Team 🙷')
    st.title('Number Of Matches Won By Each Team In IPL 2022')

    fig2 = go.Figure(data=[go.Pie(labels=cols,values=values)])
    #fig2.update_layout(title_text='Pie', title='Number of matches won by each team')
    fig2.update_layout(
    autosize=False,
    width=600,
    height=500
    )
    st.write(fig2)


    # Players name of each team
    #st.write('## 🙶 Players Name of Each Team 🙷')
    st.title('Players Name Of Each Team')

    def BatsmanAndBowlerName(TeamName):
        # Batsman Name
        TeamData = batting_data[batting_data['Team'] == TeamName]
        TeamPlayers = TeamData['PlayerName'].drop_duplicates()
        
        data = pd.DataFrame(TeamPlayers)
        data = data.reset_index()
        data.drop(columns=['index'], inplace=True)
        data.rename(columns={'PlayerName' : TeamName + ' Batsman'}, inplace=True)
        
        # Bowler Name
        TeamData2 = bowling_data[bowling_data['Team'] == TeamName]
        TeamPlayer2 = TeamData2['PlayerName'].drop_duplicates()
        
        data2 = pd.DataFrame(TeamPlayer2)
        data2 = data2.reset_index()
        data2.drop(columns=['index'], inplace=True)
        data2.rename(columns={'PlayerName' : TeamName + ' Bowlers'}, inplace=True)
        
        data[TeamName + ' Bowler'] = data['Bowler'] = data2

        data.drop(columns=['Bowler'], inplace=True)

        data = data.replace(np.nan, '-')
        
        st.table(data)

    # Teams Name
    option = st.selectbox(
        'Select The Team',
        ('RCB', 'MI', 'KKR', 'GT', 'SRH', 'RR', 'LSG', 'DC', 'CSK', 'PBSK'))

    # Calling function
    TeamName = option
    BatsmanAndBowlerName(TeamName)

    # display imag
    image = Image.open('Player.jpg')
    st.image(image)

#====>>>> TEAM INFO FUNCTION CALLING
if (selected == 'IPL Teams Info'):
    TeamsInfo()




# ANOTHER PAGE START PAGE 2
#==================================================================#
#==================================================================#
#==================================================================#

def PlayerPerformance():
    st.title('Batsman Performance In IPL 2022')

    def RunScored(player_name):
        # get the sum of total run
        player_data = batting_data[batting_data['PlayerName'] == player_name]
        run = sum(player_data['Runs'])
        
        # get the sum of balls faced by player
        balls = sum(player_data['Balls'])
        
        # get the sum of dot balls faced by player
        dot_balls = sum(player_data['DotBalls'])
        
        # get the 1 run
        one = sum(player_data['Ones'])
        
        # get the 2 run
        two = sum(player_data['Twos'])
        
        # get the 3 run
        three = sum(player_data['Threes'])
        
        # get the 4 run
        four = sum(player_data['Fours'])
        
        # get the 6 run
        six = sum(player_data['Sixes'])
        
        # strike rate
        strike = (run / balls) * 100
        
        player_data = {
        'Scores' : [one, two, three, four, six, run, balls, dot_balls, strike]
        }
        
        index = ['Single run', 'Double run', 'Triple run', 'Fours', 'Sixes', 'Total runs', 'Total balls faced', 'Total dot balls', 'Strike rate']
        df = pd.DataFrame(player_data, index)
        
        # convert all column datatype into int
        df = df.astype(int)
        
        # Plot Bar Graph
        fig1 = px.bar(df, text_auto='.2s', title = 'Peformance of ' + player_name + 'in IPL 2022', y="Scores", color='Scores', width=800)
        
        fig1.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
        
        st.write(fig1)
        
        # get all columns name
        cols = df.index
        
        # get all columns values
        values = one, two, three, four, six, run, balls, dot_balls, strike
        
        # Plot Pie Charts
        fig2 = go.Figure(data=[go.Pie(labels=cols,values=values)])

        fig2.update_layout(
        autosize=False,
        width=600,
        height=500
        )
            
        st.write(fig2)

        # data frame
        st.table(df)

    # get the all players Name
    all_player = batting_data['PlayerName']
    all_player = all_player.drop_duplicates()


    PlayersList = []
    for i in all_player:
        PlayersList.append(i)

    PlayerNameList = sorted(PlayersList)
    
    option = st.selectbox(
    'Select Your Favorite Player',
    (PlayerNameList))

    # calling function
    player_name = option
    RunScored(player_name)

    st.write('-------')

    # Top 10 high scorer batsman in IPL 2022
    #st.write('## 🙶 Top 10 high scorer batsman in IPL 2022 🙷')
    st.title('Top 10 High Scorer Batsman Of 2022')

    Top10 = {
    'Runs' : [863, 616, 508, 487, 483, 481, 468, 460, 458, 451]
    }
    index = ['Jos Buttler', 'K L Rahul', 'Quinton De Kock', 'Hardik Pandya', 'Shubman Gill', 'David Miller', 'Faf Du Plessis', 'Shikhar Dhawan', 'Sanju Samson', 'Deepak Hooda']
    Top10 = pd.DataFrame(Top10, index)

    # bar plot
    fig = px.bar(Top10, text_auto='.2s', y='Runs', color='Runs', width=800)
    fig.update_traces(textfont_size=12, textangle=0, cliponaxis=False)
    st.write(fig)

    st.write('------')

    # Number of Baundries by each player
    #st.write('## 🙶 Number of Baundries made by each player in IPL 2022 🙷')
    st.title('Number of Boundaries Made By Each Player In IPL 2022')

    def Boundary(PName):
        Name = batting_data[batting_data['PlayerName'] == PName]
        
        DF = {
            'Boundaries' : [sum(Name['Fours']), sum(Name['Sixes'])]
        }
        
        index = ['Four', 'Six']
        
        DF = pd.DataFrame(DF, index)
        fig = px.bar(DF, y = 'Boundaries', color="Boundaries", title='Number of Boundaries made by ' + PName + ' in IPL 2022',  width=820)
        st.write(fig)

    # get the all players Name
    option = ['Aaron Finch',
 'Abdul Samad', 'Abhijeet Tomar', 'Abhinav Manohar', 'Abhishek Sharma', 'Adam Milne', 'Aiden Markram', 'Ajinkya Rahane', 'Akash Deep',
 'Alzarri Joseph', 'Aman Khan', 'Ambati Rayudu', 'Andre Russell', 'Andrew Tye', 'Anmolpreet Singh', 'Anrich Nortje', 'Anuj Rawat',
 'Anukul Roy', 'Arshdeep Singh', 'Avesh Khan', 'Axar Patel', 'Ayush Badoni', 'B Indrajith', 'Basil Thampi', 'Bhanuka Rajapaksa',
 'Bhuvneshwar Kumar', 'Chetan Sakariya', 'Chris Jordan', 'Daniel Sams', 'Darshan Nalkande', 'Daryl Mitchell', 'David Miller',
 'David Warner', 'David Willey', 'Deepak Hooda', 'Devdutt Padikkal', 'Devon Conway', 'Dewald Brevis', 'Dinesh Karthik',
 'Dushmantha Chameera', 'Dwaine Pretorius', 'Dwayne Bravo', 'Evin Lewis', 'Fabian Allen', 'Faf Du Plessis', 'Fazalhaq Farooqi',
 'Glenn Maxwell', 'Hardik Pandya', 'Harpreet Brar', 'Harshal Patel', 'Harshit Rana', 'Hrithik Shokeen', 'Ishan Kishan',
 'Jagadeesan Narayan', 'Jagadeesha Suchith', 'James Neesham', 'Jason Holder', 'Jasprit Bumrah', 'Jaydev Unadkat', 'Jitesh Sharma',
 'Jonny Bairstow', 'Jos Buttler', 'Josh Hazlewood', 'K L Rahul', 'Kagiso Rabada', 'Kamlesh Nagarkoti', 'Kane Williamson',
 'Karan Sharma', 'Kartik Tyagi', 'Karun Nair', 'Khaleel Ahmed', 'Kieron Pollard', 'Krishnappa Gowtham', 'Krunal Pandya',
 'Kuldeep Sen', 'Kuldeep Yadav', 'Kumar Kartikeya Singh', 'Lalit Yadav', 'Liam Livingstone', 'Lockie Ferguson', 'MS Dhoni',
 'Maheesh Theekshana', 'Mahipal Lomror', 'Manan Vohra', 'Mandeep Singh', 'Manish Pandey', 'Marco Jansen', 'Marcus Stoinis',
 'Matheesha Pathirana', 'Matthew Wade', 'Mayank Agarwal', 'Mayank Markande', 'Mitchell Marsh', 'Mitchell Santner', 'Moeen Ali',
 'Mohammad Shami', 'Mohammed Siraj', 'Mohsin Khan', 'Mukesh Choudhary', 'Murugan Ashwin', 'Mustafizur Rahman', 'Nathan Coulter-Nile',
 'Nathan Ellis', 'Navdeep Saini', 'Nicholas Pooran', 'Nitish Rana', 'Obed McCoy', 'Odean Smith', 'Pat Cummins', 'Pradeep Sangwan',
 'Prashant Solanki', 'Prasidh Krishna', 'Prerak Mankad', 'Prithvi Shaw', 'Priyam Garg', 'Quinton De Kock', 'Rahul Chahar',
 'Rahul Tewatia', 'Rahul Tripathi', 'Rajangad Bawa', 'Rajat Patidar', 'Ramandeep Singh', 'Rashid Khan', 'Rasikh Salam',
 'Rassie van der Dussen', 'Ravi Bishnoi', 'Ravichandran Ashwin', 'Ravindra Jadeja', 'Riley Meredith', 'Rinku Singh',
 'Ripal Patel', 'Rishabh Pant', 'Rishi Dhawan', 'Riyan Parag', 'Robin Uthappa', 'Rohit Sharma', 'Romario Shepherd',
 'Rovman Powell', 'Ruturaj  Gaikwad', 'Sai Kishore', 'Sai Sudharsan', 'Sam Billings',
 'Sandeep Sharma', 'Sanjay Yadav','Sanju Samson', 'Sarfaraz Khan', 'Sean Abbott', 'Shahbaz Ahmed', 'Shahrukh Khan',
 'Shardul Thakur', 'Shashank Singh', 'Sheldon Jackson', 'Sherfane Rutherford', 'Shikhar Dhawan', 'Shimron Hetmyer',
 'Shivam Dube', 'Shivam Mavi',  'Shreyas Gopal', 'Shreyas Iyer', 'Shubman Gill', 'Siddarth Kaul', 'Simarjeet Singh',
 'Simran Singh', 'Srikar Bharat', 'Sunil Narine',  'Suryakumar Yadav', 'Suyash S Prabhudessai', 'T Natarajan', 'Tilak Varma',
 'Tim David', 'Tim Seifert',   'Tim Southee', 'Trent Boult', 'Tristan Stubbs', 'Tushar Deshpande', 'Tymal Mills', 'Umesh Yadav',
   'Umran Malik', 'Vaibhav Arora', 'Varun Aaron',   'Varun Chakaravarthy', 'Venkatesh Iyer', 'Vijay Shankar', 'Virat Kohli',
   'Wanindu Hasaranga', 'Washington Sundar', 'Wriddhiman Saha',  'Yashasvi Jaiswal', 'Yuzvendra Chahal']


    option = st.selectbox(
    'Select Your Favorite Player',
    (option))

    # calling function
    player_name = option
    Boundary(player_name)

    # function 
    st.title('Comparision Between Two Batsman')
    def BaterVsBater(name1, name2):
    
        # Player 1 performance
        player1 = batting_data[batting_data['PlayerName'] == name1]
        run1 = sum(player1['Runs'])
        balls1 = sum(player1['Balls'])
        dotballs1 = sum(player1['DotBalls'])
        fours1 = sum(player1['Fours'])
        sixes1 = sum(player1['Sixes'])
        strike1 = (run1 / balls1) * 100
        
        # Player 2 performance
        player2 = batting_data[batting_data['PlayerName'] == name2]
        run2 = sum(player2['Runs'])
        balls2 = sum(player2['Balls'])
        dotballs2 = sum(player2['DotBalls'])
        fours2 = sum(player2['Fours'])
        sixes2 = sum(player2['Sixes'])
        strike2 = (run2 / balls2) * 100
        
        print(run1, balls1, dotballs1, fours1, sixes1, strike1)
        print(run2, balls2, dotballs2, fours2, sixes2, strike2)
        
        data = {
            name1 : [run1, balls1, dotballs1, fours1, sixes1, strike1],
            name2 : [run2, balls2, dotballs2, fours2, sixes2, strike2]
        }
        
        index = ['Total Runs', 'Total Balls Faced', 'Total Dot Balls Faced', 'Fours', 'Sixes', 'Strike Rate']
        
        df = pd.DataFrame(data, index)
        
        fig = px.bar(df, title=name1 + ' Vs ' + name2, width=840)
        st.write(fig)
        
    # calling function PlayerVsPlayer
    name1 = ['Aaron Finch',
 'Abdul Samad', 'Abhijeet Tomar', 'Abhinav Manohar', 'Abhishek Sharma', 'Adam Milne', 'Aiden Markram', 'Ajinkya Rahane', 'Akash Deep',
 'Alzarri Joseph', 'Aman Khan', 'Ambati Rayudu', 'Andre Russell', 'Andrew Tye', 'Anmolpreet Singh', 'Anrich Nortje', 'Anuj Rawat',
 'Anukul Roy', 'Arshdeep Singh', 'Avesh Khan', 'Axar Patel', 'Ayush Badoni', 'B Indrajith', 'Basil Thampi', 'Bhanuka Rajapaksa',
 'Bhuvneshwar Kumar', 'Chetan Sakariya', 'Chris Jordan', 'Daniel Sams', 'Darshan Nalkande', 'Daryl Mitchell', 'David Miller',
 'David Warner', 'David Willey', 'Deepak Hooda', 'Devdutt Padikkal', 'Devon Conway', 'Dewald Brevis', 'Dinesh Karthik',
 'Dushmantha Chameera', 'Dwaine Pretorius', 'Dwayne Bravo', 'Evin Lewis', 'Fabian Allen', 'Faf Du Plessis', 'Fazalhaq Farooqi',
 'Glenn Maxwell', 'Hardik Pandya', 'Harpreet Brar', 'Harshal Patel', 'Harshit Rana', 'Hrithik Shokeen', 'Ishan Kishan',
 'Jagadeesan Narayan', 'Jagadeesha Suchith', 'James Neesham', 'Jason Holder', 'Jasprit Bumrah', 'Jaydev Unadkat', 'Jitesh Sharma',
 'Jonny Bairstow', 'Jos Buttler', 'Josh Hazlewood', 'K L Rahul', 'Kagiso Rabada', 'Kamlesh Nagarkoti', 'Kane Williamson',
 'Karan Sharma', 'Kartik Tyagi', 'Karun Nair', 'Khaleel Ahmed', 'Kieron Pollard', 'Krishnappa Gowtham', 'Krunal Pandya',
 'Kuldeep Sen', 'Kuldeep Yadav', 'Kumar Kartikeya Singh', 'Lalit Yadav', 'Liam Livingstone', 'Lockie Ferguson', 'MS Dhoni',
 'Maheesh Theekshana', 'Mahipal Lomror', 'Manan Vohra', 'Mandeep Singh', 'Manish Pandey', 'Marco Jansen', 'Marcus Stoinis',
 'Matheesha Pathirana', 'Matthew Wade', 'Mayank Agarwal', 'Mayank Markande', 'Mitchell Marsh', 'Mitchell Santner', 'Moeen Ali',
 'Mohammad Shami', 'Mohammed Siraj', 'Mohsin Khan', 'Mukesh Choudhary', 'Murugan Ashwin', 'Mustafizur Rahman', 'Nathan Coulter-Nile',
 'Nathan Ellis', 'Navdeep Saini', 'Nicholas Pooran', 'Nitish Rana', 'Obed McCoy', 'Odean Smith', 'Pat Cummins', 'Pradeep Sangwan',
 'Prashant Solanki', 'Prasidh Krishna', 'Prerak Mankad', 'Prithvi Shaw', 'Priyam Garg', 'Quinton De Kock', 'Rahul Chahar',
 'Rahul Tewatia', 'Rahul Tripathi', 'Rajangad Bawa', 'Rajat Patidar', 'Ramandeep Singh', 'Rashid Khan', 'Rasikh Salam',
 'Rassie van der Dussen', 'Ravi Bishnoi', 'Ravichandran Ashwin', 'Ravindra Jadeja', 'Riley Meredith', 'Rinku Singh',
 'Ripal Patel', 'Rishabh Pant', 'Rishi Dhawan', 'Riyan Parag', 'Robin Uthappa', 'Rohit Sharma', 'Romario Shepherd',
 'Rovman Powell', 'Ruturaj  Gaikwad', 'Sai Kishore', 'Sai Sudharsan', 'Sam Billings',
 'Sandeep Sharma', 'Sanjay Yadav','Sanju Samson', 'Sarfaraz Khan', 'Sean Abbott', 'Shahbaz Ahmed', 'Shahrukh Khan',
 'Shardul Thakur', 'Shashank Singh', 'Sheldon Jackson', 'Sherfane Rutherford', 'Shikhar Dhawan', 'Shimron Hetmyer',
 'Shivam Dube', 'Shivam Mavi',  'Shreyas Gopal', 'Shreyas Iyer', 'Shubman Gill', 'Siddarth Kaul', 'Simarjeet Singh',
 'Simran Singh', 'Srikar Bharat', 'Sunil Narine',  'Suryakumar Yadav', 'Suyash S Prabhudessai', 'T Natarajan', 'Tilak Varma',
 'Tim David', 'Tim Seifert',   'Tim Southee', 'Trent Boult', 'Tristan Stubbs', 'Tushar Deshpande', 'Tymal Mills', 'Umesh Yadav',
   'Umran Malik', 'Vaibhav Arora', 'Varun Aaron',   'Varun Chakaravarthy', 'Venkatesh Iyer', 'Vijay Shankar', 'Virat Kohli',
   'Wanindu Hasaranga', 'Washington Sundar', 'Wriddhiman Saha',  'Yashasvi Jaiswal', 'Yuzvendra Chahal']
    
    option1 = st.selectbox(
    'Select Your First Player',
    (name1))

    name2 = ['Aaron Finch',
 'Abdul Samad', 'Abhijeet Tomar', 'Abhinav Manohar', 'Abhishek Sharma', 'Adam Milne', 'Aiden Markram', 'Ajinkya Rahane', 'Akash Deep',
 'Alzarri Joseph', 'Aman Khan', 'Ambati Rayudu', 'Andre Russell', 'Andrew Tye', 'Anmolpreet Singh', 'Anrich Nortje', 'Anuj Rawat',
 'Anukul Roy', 'Arshdeep Singh', 'Avesh Khan', 'Axar Patel', 'Ayush Badoni', 'B Indrajith', 'Basil Thampi', 'Bhanuka Rajapaksa',
 'Bhuvneshwar Kumar', 'Chetan Sakariya', 'Chris Jordan', 'Daniel Sams', 'Darshan Nalkande', 'Daryl Mitchell', 'David Miller',
 'David Warner', 'David Willey', 'Deepak Hooda', 'Devdutt Padikkal', 'Devon Conway', 'Dewald Brevis', 'Dinesh Karthik',
 'Dushmantha Chameera', 'Dwaine Pretorius', 'Dwayne Bravo', 'Evin Lewis', 'Fabian Allen', 'Faf Du Plessis', 'Fazalhaq Farooqi',
 'Glenn Maxwell', 'Hardik Pandya', 'Harpreet Brar', 'Harshal Patel', 'Harshit Rana', 'Hrithik Shokeen', 'Ishan Kishan',
 'Jagadeesan Narayan', 'Jagadeesha Suchith', 'James Neesham', 'Jason Holder', 'Jasprit Bumrah', 'Jaydev Unadkat', 'Jitesh Sharma',
 'Jonny Bairstow', 'Jos Buttler', 'Josh Hazlewood', 'K L Rahul', 'Kagiso Rabada', 'Kamlesh Nagarkoti', 'Kane Williamson',
 'Karan Sharma', 'Kartik Tyagi', 'Karun Nair', 'Khaleel Ahmed', 'Kieron Pollard', 'Krishnappa Gowtham', 'Krunal Pandya',
 'Kuldeep Sen', 'Kuldeep Yadav', 'Kumar Kartikeya Singh', 'Lalit Yadav', 'Liam Livingstone', 'Lockie Ferguson', 'MS Dhoni',
 'Maheesh Theekshana', 'Mahipal Lomror', 'Manan Vohra', 'Mandeep Singh', 'Manish Pandey', 'Marco Jansen', 'Marcus Stoinis',
 'Matheesha Pathirana', 'Matthew Wade', 'Mayank Agarwal', 'Mayank Markande', 'Mitchell Marsh', 'Mitchell Santner', 'Moeen Ali',
 'Mohammad Shami', 'Mohammed Siraj', 'Mohsin Khan', 'Mukesh Choudhary', 'Murugan Ashwin', 'Mustafizur Rahman', 'Nathan Coulter-Nile',
 'Nathan Ellis', 'Navdeep Saini', 'Nicholas Pooran', 'Nitish Rana', 'Obed McCoy', 'Odean Smith', 'Pat Cummins', 'Pradeep Sangwan',
 'Prashant Solanki', 'Prasidh Krishna', 'Prerak Mankad', 'Prithvi Shaw', 'Priyam Garg', 'Quinton De Kock', 'Rahul Chahar',
 'Rahul Tewatia', 'Rahul Tripathi', 'Rajangad Bawa', 'Rajat Patidar', 'Ramandeep Singh', 'Rashid Khan', 'Rasikh Salam',
 'Rassie van der Dussen', 'Ravi Bishnoi', 'Ravichandran Ashwin', 'Ravindra Jadeja', 'Riley Meredith', 'Rinku Singh',
 'Ripal Patel', 'Rishabh Pant', 'Rishi Dhawan', 'Riyan Parag', 'Robin Uthappa', 'Rohit Sharma', 'Romario Shepherd',
 'Rovman Powell', 'Ruturaj  Gaikwad', 'Sai Kishore', 'Sai Sudharsan', 'Sam Billings',
 'Sandeep Sharma', 'Sanjay Yadav','Sanju Samson', 'Sarfaraz Khan', 'Sean Abbott', 'Shahbaz Ahmed', 'Shahrukh Khan',
 'Shardul Thakur', 'Shashank Singh', 'Sheldon Jackson', 'Sherfane Rutherford', 'Shikhar Dhawan', 'Shimron Hetmyer',
 'Shivam Dube', 'Shivam Mavi',  'Shreyas Gopal', 'Shreyas Iyer', 'Shubman Gill', 'Siddarth Kaul', 'Simarjeet Singh',
 'Simran Singh', 'Srikar Bharat', 'Sunil Narine',  'Suryakumar Yadav', 'Suyash S Prabhudessai', 'T Natarajan', 'Tilak Varma',
 'Tim David', 'Tim Seifert',   'Tim Southee', 'Trent Boult', 'Tristan Stubbs', 'Tushar Deshpande', 'Tymal Mills', 'Umesh Yadav',
   'Umran Malik', 'Vaibhav Arora', 'Varun Aaron',   'Varun Chakaravarthy', 'Venkatesh Iyer', 'Vijay Shankar', 'Virat Kohli',
   'Wanindu Hasaranga', 'Washington Sundar', 'Wriddhiman Saha',  'Yashasvi Jaiswal', 'Yuzvendra Chahal']

    option2 = st.selectbox(
        'Select Your Second Player',
        (name2)
    )

    

    # calling function
    name1 = option1
    name2 = option2
    BaterVsBater(name1, name2)
    
#====>>>> BATSMAN PERFORMANCE FUNCTION CALLING
if (selected == 'Batsman Performance'):
    PlayerPerformance()




# ANOTHER PAGE START PAGE 3
#==================================================================#
#==================================================================#
#==================================================================#

def BowlerPerformance():
    st.title('Bowlers Performance In IPL 2022 ')

    def BowlerDataIPL(BowlerNameIs):
        BowlerNameList = bowling_data['PlayerName'].drop_duplicates()
        BowlerNameList = sorted(BowlerNameList)

        bowlp = bowling_data[bowling_data['PlayerName'] == BowlerNameIs]
    
        # get the number of over
        Over = sum(bowlp['Overs'])
    
        # maidens
        Maidens = sum(bowlp['Maidens'])
    
        # Runs
        Runs = sum(bowlp['Runs'])
        
        # Wickets
        Wickets = sum(bowlp['Wickets'])
        
        # Wides
        Wides = sum(bowlp['Wides'])
        
        # No Balls
        NoBalls = sum(bowlp['NoBalls'])
    
        # Economy
        Economy = Runs / Over
        
        # DotBalls
        DotBalls = sum(bowlp['DotBalls'])
        
        # Balles
        Balls = Over * 6
    
        # create dataframe
        BowlPlayerData = {
        'IPL 2022 Bowler status' : [Over, Maidens, Runs, Wickets, Wides, Balls, NoBalls, DotBalls, Economy]
        }
        
        index = ['Over', 'Maidens', 'Runs', 'Wickets', 'Wides', 'Balls', 'NoBalls', 'DotBalls', 'Economy']
        
        df = pd.DataFrame(BowlPlayerData, index)
    
        # Bar graph
        fig1 = px.bar(df, text_auto='.2s', y='IPL 2022 Bowler status' , title='Performance of ' + BowlerNameIs + ' in IPL 2022', color='IPL 2022 Bowler status', width=880)
        st.write(fig1)
        
        # Pie chart
        cols = df.index
        values = Over, Maidens, Runs, Wickets, Wides, Balls, NoBalls, DotBalls, Economy
        
        fig2 = go.Figure(data=[go.Pie(labels=cols,values=values)])
        
        st.write(fig2)
    
        # data frame
        st.table(df)


    # load data
    BowlerNameList = bowling_data['PlayerName'].drop_duplicates()
    BowlerNameList = sorted(BowlerNameList)

    option = st.selectbox(
        'Select Your Favorite Player',
        (BowlerNameList))

    # calling Bowler function
    BowlerNameIs = option
    BowlerDataIPL(BowlerNameIs)

    st.write('------')

    # 🙶 Top 10 most wicket takker bowler in IPL 2022 🙷
    #st.write('## 🙶 Top 10 most wicket taker bowler in IPL 2022 🙷')
    st.title('Top 10 Most Wicket Taker Bowler Of 2022')

    data = {
    'Wickets' : [27, 26, 23, 22, 21, 20, 20, 19, 19, 19]
    }

    index = ['Yuzvendra Chahal', 'Wanindu Hasaranga', 'Kagiso Rabada', 'Umran Malik', 'Kuldeep Yadav', 'Mohammad Shami', 'Josh Hazlewood', 'Rashid Khan', 'Harshal Patel', 'Prasidh Krishna']

    data = pd.DataFrame(data, index)

    fig = px.bar(data, text_auto='.2s', y='Wickets', color='Wickets', )
    st.write(fig)

    st.write('-----')

    # bowler vs bowler performance
    st.title('Comparision Between Two Bowlers')
    def BowlerVsBowler(name1, name2):
    
    # Bowler 1
        BowlerName1 = bowling_data[bowling_data['PlayerName'] == name1]
        Over1 = sum(BowlerName1['Overs'])
        Maidens1 = sum(BowlerName1['Maidens'])
        Wickets1 = sum(BowlerName1['Wickets'])
        DotBall1 = sum(BowlerName1['DotBalls'])

        # Calculate economy
        Runs1 = sum(BowlerName1['Runs'])
        Economy1 = Runs1 / Over1
        
        # Bowler 2
        BowlerName2 = bowling_data[bowling_data['PlayerName'] == name2]
        Over2 = sum(BowlerName2['Overs'])
        Maidens2 = sum(BowlerName2['Maidens'])
        Wickets2 = sum(BowlerName2['Wickets'])
        DotBall2 = sum(BowlerName2['DotBalls'])

        # Calculate economy
        Runs2 = sum(BowlerName2['Runs'])
        Economy2 = Runs2 / Over2
        
        data = {
            name1 : [Over1, Maidens1, Wickets1, DotBall1, Economy1],
            name2 : [Over2, Maidens2, Wickets2, DotBall2, Economy2]
        }
        
        index = ['Overs', 'Maiden Overs', 'Total Wickets', 'Total Dot Balls', 'Economy']
        df = pd.DataFrame(data, index)
        fig = px.bar(df, title=name1 + ' Vs ' + name2, width=865)
        st.write(fig)

    # function calling BowlerVsBowler
    BowlerList1 = ['Abdul Samad', 'Abhishek Sharma', 'Adam Milne', 'Aiden Markram', 'Akash Deep', 'Alzarri Joseph', 'Aman Khan',
 'Andre Russell', 'Andrew Tye', 'Anrich Nortje', 'Arshdeep Singh', 'Avesh Khan', 'Axar Patel', 'Ayush Badoni', 'Basil Thampi',
 'Bhuvneshwar Kumar', 'Chetan Sakariya', 'Chris Jordan', 'Daniel Sams', 'Darshan Nalkande', 'Daryl Mitchell', 'David Willey',
 'Deepak Hooda', 'Dewald Brevis', 'Dushmantha Chameera', 'Dwaine Pretorius', 'Dwayne Bravo', 'Fabian Allen', 'Fazalhaq Farooqi',
 'Glenn Maxwell', 'Hardik Pandya', 'Harpreet Brar', 'Harshal Patel', 'Harshit Rana', 'Hrithik Shokeen', 'Jagadeesha Suchith',
 'James Neesham', 'Jason Holder', 'Jasprit Bumrah', 'Jaydev Unadkat', 'Josh Hazlewood', 'Kagiso Rabada', 'Kamlesh Nagarkoti',
 'Kartik Tyagi', 'Khaleel Ahmed', 'Kieron Pollard', 'Krishnappa Gowtham', 'Krunal Pandya', 'Kuldeep Sen', 'Kuldeep Yadav',
 'Kumar Kartikeya Singh', 'Lalit Yadav', 'Liam Livingstone', 'Lockie Ferguson', 'Maheesh Theekshana', 'Mahipal Lomror',
 'Marco Jansen', 'Marcus Stoinis', 'Matheesha Pathirana', 'Mayank Markande', 'Mitchell Marsh', 'Mitchell Santner',
 'Moeen Ali', 'Mohammad Shami', 'Mohammed Siraj', 'Mohsin Khan', 'Mukesh Choudhary', 'Murugan Ashwin', 'Mustafizur Rahman',
 'Nathan Coulter-Nile', 'Nathan Ellis', 'Navdeep Saini', 'Nitish Rana', 'Obed McCoy', 'Odean Smith', 'Pat Cummins', 'Pradeep Sangwan',
 'Prashant Solanki', 'Prasidh Krishna', 'Rahul Chahar', 'Rahul Tewatia', 'Ramandeep Singh', 'Rashid Khan', 'Rasikh Salam',
 'Ravi Bishnoi', 'Ravichandran Ashwin', 'Ravindra Jadeja', 'Riley Meredith', 'Rishi Dhawan', 'Riyan Parag', 'Romario Shepherd',
 'Rovman Powell', 'Sai Kishore', 'Sandeep Sharma', 'Sanjay Yadav', 'Sean Abbott', 'Shahbaz Ahmed', 'Shardul Thakur', 'Shashank Singh',
 'Shivam Dube', 'Shivam Mavi', 'Shreyas Gopal', 'Shreyas Iyer', 'Siddarth Kaul', 'Simarjeet Singh', 'Sunil Narine', 'T Natarajan',
 'Tilak Varma', 'Tim Southee', 'Trent Boult', 'Tushar Deshpande', 'Tymal Mills', 'Umesh Yadav', 'Umran Malik', 'Vaibhav Arora',
 'Varun Aaron', 'Varun Chakaravarthy', 'Venkatesh Iyer', 'Vijay Shankar', 'Wanindu Hasaranga', 'Washington Sundar', 'Yash Dayal', 
 'Yashasvi Jaiswal', 'Yuzvendra Chahal']

 

    BowlerList2 = ['Abdul Samad', 'Abhishek Sharma', 'Adam Milne', 'Aiden Markram', 'Akash Deep', 'Alzarri Joseph', 'Aman Khan',
 'Andre Russell', 'Andrew Tye', 'Anrich Nortje', 'Arshdeep Singh', 'Avesh Khan', 'Axar Patel', 'Ayush Badoni', 'Basil Thampi',
 'Bhuvneshwar Kumar', 'Chetan Sakariya', 'Chris Jordan', 'Daniel Sams', 'Darshan Nalkande', 'Daryl Mitchell', 'David Willey',
 'Deepak Hooda', 'Dewald Brevis', 'Dushmantha Chameera', 'Dwaine Pretorius', 'Dwayne Bravo', 'Fabian Allen', 'Fazalhaq Farooqi',
 'Glenn Maxwell', 'Hardik Pandya', 'Harpreet Brar', 'Harshal Patel', 'Harshit Rana', 'Hrithik Shokeen', 'Jagadeesha Suchith',
 'James Neesham', 'Jason Holder', 'Jasprit Bumrah', 'Jaydev Unadkat', 'Josh Hazlewood', 'Kagiso Rabada', 'Kamlesh Nagarkoti',
 'Kartik Tyagi', 'Khaleel Ahmed', 'Kieron Pollard', 'Krishnappa Gowtham', 'Krunal Pandya', 'Kuldeep Sen', 'Kuldeep Yadav',
 'Kumar Kartikeya Singh', 'Lalit Yadav', 'Liam Livingstone', 'Lockie Ferguson', 'Maheesh Theekshana', 'Mahipal Lomror',
 'Marco Jansen', 'Marcus Stoinis', 'Matheesha Pathirana', 'Mayank Markande', 'Mitchell Marsh', 'Mitchell Santner',
 'Moeen Ali', 'Mohammad Shami', 'Mohammed Siraj', 'Mohsin Khan', 'Mukesh Choudhary', 'Murugan Ashwin', 'Mustafizur Rahman',
 'Nathan Coulter-Nile', 'Nathan Ellis', 'Navdeep Saini', 'Nitish Rana', 'Obed McCoy', 'Odean Smith', 'Pat Cummins', 'Pradeep Sangwan',
 'Prashant Solanki', 'Prasidh Krishna', 'Rahul Chahar', 'Rahul Tewatia', 'Ramandeep Singh', 'Rashid Khan', 'Rasikh Salam',
 'Ravi Bishnoi', 'Ravichandran Ashwin', 'Ravindra Jadeja', 'Riley Meredith', 'Rishi Dhawan', 'Riyan Parag', 'Romario Shepherd',
 'Rovman Powell', 'Sai Kishore', 'Sandeep Sharma', 'Sanjay Yadav', 'Sean Abbott', 'Shahbaz Ahmed', 'Shardul Thakur', 'Shashank Singh',
 'Shivam Dube', 'Shivam Mavi', 'Shreyas Gopal', 'Shreyas Iyer', 'Siddarth Kaul', 'Simarjeet Singh', 'T Natarajan',
 'Tilak Varma', 'Tim Southee', 'Trent Boult', 'Tushar Deshpande', 'Tymal Mills', 'Umesh Yadav', 'Umran Malik', 'Vaibhav Arora',
 'Varun Aaron', 'Varun Chakaravarthy', 'Venkatesh Iyer', 'Vijay Shankar', 'Wanindu Hasaranga', 'Washington Sundar', 'Yash Dayal', 
 'Yashasvi Jaiswal', 'Yuzvendra Chahal']

    
    option1 = st.selectbox(
        'Select Your First Player',
        (BowlerList1))

    option2 = st.selectbox(
        'Select Your Second Player',
        (BowlerList2))

    name1 = option1
    name2 = option2
    BowlerVsBowler(name1, name2)

#====>>>> Bowler Performance function calling 🙶🙷
if (selected == 'Bowler Performance'):
    BowlerPerformance()
    