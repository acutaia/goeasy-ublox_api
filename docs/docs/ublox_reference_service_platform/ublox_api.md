It is a Python-based software developed exploited the async paradigm through the FastAPI framework. During
boot, it interacts with Keycloak server and dynamically configures the OAuth2 security settings of the exposed
REST endpoints. The main purpose is to provide a public and secure interface to let SERENGETI, or other
systems, to obtain secure Galileo data to be used as reference. The data extraction interfaces allow the
parametrization of the specific satellite and timeframe of interest. When it receives a request, granted via
Oauth2 tokens, it extracts from the PostgreSQL database the raw information of interest and embed them in
a JSON response. It is in charge to feed the GOEASY platform with the necessary data to apply comparison
and thresholds algorithms for the third-party lbs-data that needs to be authenticated.