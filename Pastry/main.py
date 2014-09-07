import operations
import helper
from node import MyNode

A = MyNode(helper.generateIpAddress())
X = MyNode(helper.generateIpAddress())
operations.route(A, X)