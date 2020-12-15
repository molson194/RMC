Action Items
* Give Feedback
  * UI - Rate 1..5 on 2 categories, 2 written responses
  * POST givefeedback api - add object to db + allow empty
  * Validate the access token
  * Send receiver an email when new feedback arrives
* MyFeedback
  * Prep myfeedback UI
  * GET myfeedback list api + Respond with hard-coded list + Populate UI
  * Validate the access token
  * Create myfeedback collection + query collection + serialize response
  * GET aggregate myfeedback api (average stars for categories) 
  * If valid access token on main page, provide 'Take me to my dashboard link'
  * Handle isempty/notrated cases
* PastFeedback
* Home page
  * If validated access token, button take me to dashboard + user name instead of login
* Validate the access token
  * If expired access token or does not exist, validate refresh token
  * If expired refresh token or does not exist, sign out the user
  * If valid refresh token, generate new access token and set cookie
  * Make this a common library

Advice for Static Web App Team
* Function logs by default (create AppInsights and link)
* Click function to view content