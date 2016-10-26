"""
Program: project1.py
Author: Cameron Armstrong
Last date modified: 15/4/14

Collects votes parsed from a ballot papers file and a candidates list file
and displays the results of the votes and counts the formal and infomal votes.
"""

import os

def getCandidates(f):
	candidates = []
	currentDirectoryPath = os.getcwd()
	listOfFileNames = os.listdir(currentDirectoryPath)
	for name in listOfFileNames:
		if name == f:
			candidatesFile = open(f, 'r')
			for line in candidatesFile:
				line = line.strip()
				if (line == ""):
					continue
				candidates.append(line)
			return candidates
	print(f, "does not exist.")
	return candidates

def parseVote(s):
	if (s == "" or s == " "):
		return 0
	
	s = s.strip()	

	if not s.isdigit():
		return -1

	return int(s)

def parsePaper(s, n):
	paper = []
	votes = s.split(',')
	sumOfVote = 0
	parsedVotes = []
	for vote in votes:
		vote = parseVote(vote)
		parsedVotes.append(vote)
		sumOfVote += vote
		if vote == -1:
			votes = [""]
			paper.append(votes)
			paper.append("non-digits")
			return paper
	if sumOfVote == 0 or len(votes) < n:
		votes = [""]
		paper.append(votes)
		paper.append("blank")
		return paper
	if len(votes) > n:
			votes = [""]
			paper.append(votes)
			paper.append("too long")
			return paper
	paper.append(parsedVotes)
	paper.append("")
	return paper

def getPapers(f, n):
	papers = []
	currentDirectoryPath = os.getcwd()
	listOfFileNames = os.listdir(currentDirectoryPath)
	for name in listOfFileNames:
		if name == f:
			papersFile = open(f, 'r')
			for line in papersFile:
				paper = parsePaper(line, n)
				if paper[1] == "":
					papers.append(parsePaper(line, n))
			return papers
	print("File", f, "not found.")
	return papers

def normalisePaper(p, n): # sum(p) > 0
	normal = []
	if p == []:
		return normal
	if p[1] == "":
		for line in p[0]:
			vote = float(line) / sum(p[0])
			normal.append(vote)
		while len(normal) < n:
			normal.append(0.0)
	return normal

def normalisePapers(ps, n): # for every p on ps, sum(p) > 0
	normalised = []
	for paper in ps:
		normalised.append(normalisePaper(paper, n))
	return normalised

def countVotes(cs, ps): # ps have been normalised for an election with len(cs) candidates
	counts = []
	countedVotes = []
	finalCount = []
	for can in cs:
		counts.append(0.0)
	for index in range(0, len(cs)):
		for page in ps:
			if len(page) > 0:
				counts[index] += page[index]
		countedVotes = []
		countedVotes.append(round(counts[index],2))
		countedVotes.append(cs[index])
		finalCount.append(countedVotes)
	finalCount.sort(reverse = True)
	return finalCount 

def printCount(c):
	for result in c:
		print(result[0], result[1])

def main():
	canFile = input("Candidates list filename: ")
	papersFile = input("Ballot papers filename: ")
	candidates = getCandidates(canFile)
	if not candidates == []:
		papers = getPapers(papersFile, len(candidates))
		numberOfVotes = len(papers)
		if not papers == []:
			papers = normalisePapers(papers, len(candidates))
			votes = countVotes(candidates, papers) 
			print("Nerdvanian election 2014\n")
			print("There were", numberOfVotes-len(votes), "informal votes")
			print("There were", len(papers), "formal votes\n")
			printCount(votes)

main()
