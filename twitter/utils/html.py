from __future__ import annotations

from bs4 import BeautifulSoup


def parse_oauth_html(html: str) -> tuple[str | None, str | None, str | None]:
    """
    :return: authenticity_token, redirect_url, redirect_after_login_url
    """
    soup = BeautifulSoup(html, "lxml")
    authenticity_token_element = soup.find("input", {"name": "authenticity_token"})
    authenticity_token = (
        authenticity_token_element.get("value") if authenticity_token_element else None
    )
    redirect_url_element = soup.find("a", text="click here to continue")
    redirect_url = redirect_url_element.get("href") if redirect_url_element else None
    redirect_after_login_element = soup.find("input", {"name": "redirect_after_login"})
    redirect_after_login_url = (
        redirect_after_login_element.get("value")
        if redirect_after_login_element
        else None
    )
    return authenticity_token, redirect_url, redirect_after_login_url


def parse_unlock_html(
    html: str,
) -> tuple[str | None, str | None, bool, bool, bool, bool, bool, bool]:
    """
    :return: authenticity_token, assignment_token, needs_unlock, start_button, finish_button, delete_button, java_script_not_available
    """
    soup = BeautifulSoup(html, "lxml")
    authenticity_token_element = soup.find("input", {"name": "authenticity_token"})
    authenticity_token = (
        authenticity_token_element.get("value") if authenticity_token_element else None
    )
    assignment_token_element = soup.find("input", {"name": "assignment_token"})
    assignment_token = (
        assignment_token_element.get("value") if assignment_token_element else None
    )
    verification_string = soup.find("input", id="verification_string")
    needs_unlock = bool(verification_string)
    start_button = bool(soup.find("input", value="Start"))
    finish_button = bool(soup.find("input", value="Continue to X"))
    delete_button = bool(soup.find("input", value="Delete"))
    email_unlock = bool(soup.find("input", value="Send email")) or bool(
        soup.find("title", string="Verify email")
    )
    java_script_not_available = bool(
        soup.find("h1", string="JavaScript is not available.")
    )
    return (
        authenticity_token,
        assignment_token,
        needs_unlock,
        email_unlock,
        start_button,
        finish_button,
        delete_button,
        java_script_not_available,
    )
