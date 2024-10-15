from typing import AnyStr, Optional, Type, Any
import requests
from bs4 import BeautifulSoup
from gentopia.tools.basetool import *

class NewsAggregatorArgs(BaseModel):
    keywords: str = Field(..., description="Keywords to search for in news headlines.")

class NewsAggregator(BaseTool):
    name = "news_aggregator"
    description = "Aggregate news headlines from multiple sources."
    args_schema: Optional[Type[BaseModel]] = NewsAggregatorArgs

    def _run(self, keywords: AnyStr) -> AnyStr:
        return self._aggregate_news(keywords)

    def _aggregate_news(self, keywords: AnyStr) -> AnyStr:
        sources = [
            ("BBC", f"https://www.bbc.co.uk/search?q={keywords.replace(' ', '+')}"),
            ("CNN", f"https://edition.cnn.com/search?q={keywords.replace(' ', '+')}"),
            ("Reuters", f"https://www.reuters.com/search/news?blob={keywords.replace(' ', '+')}")
        ]
        headlines = []
        for source, url in sources:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            for headline in soup.find_all('h3'):
                headlines.append(f"{source}: {headline.get_text()}")
        return "\n".join(headlines)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    keywords = "technology"  # Example keywords
    aggregator = NewsAggregator()
    news = aggregator._run(keywords)
    print(news)