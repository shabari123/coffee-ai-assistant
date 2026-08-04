from app.agents.router_agent import RouterAgent
from app.models.agent_context import AgentContext
from app.services.preference_extractor import PreferenceExtractor
from app.services.conversation_service import ConversationService
from app.services.preference_service import PreferenceService
from app.services.workflow_service import WorkflowService
from app.exceptions.llm_exception import LLMException
from app.constants.workflows import RECOMMENDATION_WORKFLOW


class ChatService:
    def __init__( self, router_agent: RouterAgent,
                 conversation_service: ConversationService,
                 preference_service: PreferenceService, preference_extractor: PreferenceExtractor):
        self.router_agent = router_agent
        self.conversation_service = conversation_service
        self.preference_service = preference_service
        self.preference_extractor = preference_extractor
        self.workflow_service = WorkflowService()

    def chat(self, session_id: str, message: str) -> str:
        extraction = self.preference_extractor.extract(message)
        self.preference_service.update_from_extraction(session_id, extraction)
        self.conversation_service.add_user_message(session_id, message)
        history = self.conversation_service.get_history(session_id)
        context = AgentContext(session_id=session_id, messages=history)
        workflow = self.workflow_service.get(session_id)
        try:
            if workflow == RECOMMENDATION_WORKFLOW:
                response = self.router_agent.recommendation_agent.chat(context)
            else:
                response = self.router_agent.chat(message, context)
        except LLMException as e:
            response = (
        "I'm sorry, our AI assistant is temporarily unavailable. "
        "Please try again in a few moments."
    )
        self.conversation_service.add_assistant_message(session_id, response)
        return response