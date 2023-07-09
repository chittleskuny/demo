using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Demo
{
    public class KdTreeNode<T> : BinaryTreeNode<T>
    {
        public readonly int Dimension;

        public KdTreeNode (int dimension)
        {
            Dimension = dimension;
        }

        public virtual void BinarySpacePartitioning(List<T> data) { }
    }

    public class KdTree<T> : BinaryTree<T>
    {
        public readonly int Dimension;

        public KdTree(int dimension)
        {
            Dimension = dimension;
        }
    }
}
