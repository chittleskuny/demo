using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Demo
{
    /// <summary>
    /// 二叉树节点。
    /// </summary>
    /// <typeparam name="T"></typeparam>
    public class BinaryTreeNode<T> : TreeNode<T>
    {
        public BinaryTreeNode<T>? LeftChild = null;

        public BinaryTreeNode<T>? RightChild = null;

        public override List<TreeNode<T>> Children
        {
            get
            {
                var children = new List<TreeNode<T>>();
                if (LeftChild != null)
                {
                    children.Add(LeftChild);
                }
                if (RightChild != null)
                {
                    children.Add(RightChild);
                }
                return children;
            }
        }

        /// <summary>
        /// 中序遍历。
        /// </summary>
        /// <returns></returns>
        public virtual List<T> InorderTraversal()
        {
            var all = new List<T>();
            if (LeftChild != null)
            {
                all.AddRange(LeftChild.InorderTraversal());
            }
            if (Data != null)
            {
                all.AddRange(Data);
            }
            if (RightChild != null)
            {
                all.AddRange(RightChild.InorderTraversal());
            }
            return all;
        }
    }

    /// <summary>
    /// 二叉树。
    /// </summary>
    /// <typeparam name="T"></typeparam>
    public class BinaryTree<T> : Tree<T>
    {
    }
}
