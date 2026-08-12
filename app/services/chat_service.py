from app.agents.router_agent import RouterAgent
from app.models.agent_context import AgentContext
from app.models.chat_response import ChatResponse
from app.services.preference_extractor import PreferenceExtractor
from app.services.conversation_service import ConversationService
from app.services.preference_service import PreferenceService
from app.services.workflow_service import WorkflowService
from app.exceptions.llm_exception import LLMException
from app.constants.workflows import RECOMMENDATION_WORKFLOW


class ChatService:

    def __init__(
        self,
        router_agent: RouterAgent,
        conversation_service: ConversationService,
        preference_service: PreferenceService,
        preference_extractor: PreferenceExtractor,
        workflow_service: WorkflowService,
    ):
        self.router_agent = router_agent
        self.conversation_service = conversation_service
        self.preference_service = preference_service
        self.preference_extractor = preference_extractor
        self.workflow_service = workflow_service

    def chat(
        self,
        session_id: str,
        message: str,
    ) -> ChatResponse:

        try:

            # --------------------------------------------------
            # 1. Save user message
            # --------------------------------------------------

            self.conversation_service.add_user_message(
                session_id,
                message,
            )

            # --------------------------------------------------
            # 2. Build conversation context
            # --------------------------------------------------

            history = self.conversation_service.get_history(
                session_id
            )

            context = AgentContext(
                session_id=session_id,
                messages=history,
            )

            # --------------------------------------------------
            # 3. Check active workflow
            # --------------------------------------------------

            workflow = self.workflow_service.get(
                session_id
            )

            # --------------------------------------------------
            # 4. If recommendation workflow is active,
            #    first check whether this message contains
            #    a recommendation preference.
            # --------------------------------------------------

            if workflow == RECOMMENDATION_WORKFLOW:

                extraction = self.preference_extractor.extract(
                    message
                )

                has_preference = any(
                    value is not None
                    for value in [
                        extraction.bean_type,
                        extraction.brew_method,
                        extraction.strength,
                    ]
                )

                if has_preference:

                    # User is answering the recommendation
                    # questions.

                    self.preference_service.update_from_extraction(
                        session_id,
                        extraction,
                    )

                    agent_response = (
                        self.router_agent.recommendation_agent.chat(
                            context
                        )
                    )

                else:

                    # User did not provide a recommendation
                    # preference. They may have changed intent.

                    self.workflow_service.clear(
                        session_id
                    )

                    agent_name = self.router_agent.route(
                        message
                    )

                    agent_response = self.router_agent.chat(
                        message,
                        context,
                        agent_name=agent_name,
                    )

            # --------------------------------------------------
            # 5. No active workflow
            # --------------------------------------------------

            else:

                agent_name = self.router_agent.route(
                    message
                )

                # If this is the beginning of a recommendation
                # conversation, extract preferences first.

                if agent_name == "RecommendationAgent":

                    extraction = (
                        self.preference_extractor.extract(
                            message
                        )
                    )

                    self.preference_service.update_from_extraction(
                        session_id,
                        extraction,
                    )

                agent_response = self.router_agent.chat(
                    message,
                    context,
                    agent_name=agent_name,
                )

        except LLMException:

            return ChatResponse(
                response=(
                    "I'm sorry, our AI assistant is temporarily "
                    "unavailable. Please try again in a few moments."
                ),
                products=[],
            )

        # --------------------------------------------------
        # 6. Save assistant response
        # --------------------------------------------------

        self.conversation_service.add_assistant_message(
            session_id,
            agent_response.response,
        )

        # --------------------------------------------------
        # 7. Return response
        # --------------------------------------------------

        return ChatResponse(
            response=agent_response.response,
            products=agent_response.products,
        )