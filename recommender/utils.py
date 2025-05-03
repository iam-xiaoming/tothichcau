# import boto3
# from games.models import Game, DLC

# personalize_rt = boto3.client('personalize-runtime')

# def get_aws_recommended_items(recommenderArn, userId, numResults=10, filterArn=None):
#     try:
#         params = {
#             'recommenderArn': recommenderArn,
#             'userId': userId,
#             'numResults': numResults
#         }
#         if filterArn:
#             params['filterArn'] = filterArn

#         response = personalize_rt.get_recommendations(**params)
        
#         status_code = response.get('ResponseMetadata', {}).get('HTTPStatusCode')
#         if status_code != 200:
#             print(f"Error: HTTP Status Code {status_code}")
#             return None

#         return response.get('itemList', [])

#     except Exception as e:
#         print('Exception occurred while getting recommendations:', str(e))
#         return None


# def aws_validators_recommendation(items):
#     games = Game.objects.filter(id__in=items).all()
#     dlcs = DLC.objects.filter(id__in=items).all()
#     return list(games) + list(dlcs)