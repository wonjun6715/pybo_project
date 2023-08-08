# views 디렉터리에 잇는 모든 뷰 파일 함수를 import 했으므로 pybo/urls.py와 같은 다른 모듈에서 views 모듈의 함수를 사용하는 부분을 수정할 필요 x
from .base_views import *
from .question_views import *
from .answer_views import *