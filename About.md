# About
This project is a web app used during the technical interview portion of a candidate's hiring process.
It was concieved to improve the interview process of a previous employer, which made use of excel spreadsheets.

The interviewer uses the app to store questions which will be asked in the interview.
Since questions are technical in nature, they are grouped into subareas and areas, which allow for better data visualization.
The user can create a bundle of question to be asked in an interview, this bundle is called a template.

Before each interview, the user inputs the position for which the interview is being made, the candidates name and choose a template.
The app renders a table with the questions for the interview, the expected answer and a form where the interviewers can select a score.

After completing the interview and finishing the process, the interview will be stored in the base and the interviewer will be presented with a report.
The report contains the overall score for the candidate, metrics as well as charts indicating how well the candidate did in each topic.

Lastly, the app allows for the comparasion of interviews.
The comparasion is done by selecting the interviews and generatinc comparative bar charts.

Overall, the app attempts to improve the decision making of which candidate is the best fit for a position.
I developed this as a proof of concept while learning django.
The solution was presented to my supervisor which then got introduced to the managers who really enjoyed the solution and deployed it as part of the company's interview process.

# Screenshots

# Tech Stack
The app was written in Django and uses Postgre as the database.
The python dependency managemeent is done using poetry.

The app was configured to run from within containers and its development was made entirely from within docker.
The repo contains a docker-compose for development and scripts for a (incomplete) production build.
